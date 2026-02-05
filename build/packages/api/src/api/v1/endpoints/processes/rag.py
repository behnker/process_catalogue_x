"""Process RAG assessment endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user, require_role
from src.core.tenancy import get_tenant_db
from src.models.issue_log import IssueLog
from src.models.process import Process
from src.schemas.rag_assessment import (
    RAGAssessmentRequest,
    RAGAssessmentResponse,
    RAGHistoryEntry,
    RAGHistoryResponse,
    RAGRecalculateRequest,
    RAGRecalculateResponse,
    RAGSummaryItem,
    RAGSummaryResponse,
)

router = APIRouter()

DIMENSION_COLS = {
    "people": "rag_people",
    "process": "rag_process",
    "system": "rag_system",
    "data": "rag_data",
}


@router.post("/{process_id}/rag-assessment", response_model=RAGAssessmentResponse)
async def set_rag_assessment(
    process_id: str,
    body: RAGAssessmentRequest,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Set explicit RAG assessment for a process dimension.

    BR-12: Cannot set GREEN if there are open issues in that classification.
    """
    result = await db.execute(
        select(Process).where(
            Process.id == process_id,
            Process.organization_id == user.organization_id,
        )
    )
    process = result.scalar_one_or_none()

    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    # BR-12: Block GREEN if open issues exist for this dimension
    if body.status == "green":
        open_issues = await db.execute(
            select(IssueLog.id).where(
                IssueLog.process_id == process_id,
                IssueLog.issue_classification == body.dimension,
                IssueLog.issue_status.in_(["open", "in_progress"]),
            )
        )
        open_issue_ids = [row[0] for row in open_issues.fetchall()]

        if open_issue_ids:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "Cannot set GREEN with open issues",
                    "dimension": body.dimension,
                    "open_issue_count": len(open_issue_ids),
                    "open_issue_ids": open_issue_ids[:5],  # Return first 5
                },
            )

    # Get current status
    col_name = DIMENSION_COLS[body.dimension]
    old_status = getattr(process, col_name) or "neutral"

    # Update dimension
    setattr(process, col_name, body.status)
    process.rag_last_reviewed = datetime.now(timezone.utc)
    process.rag_reviewed_by = user.id

    await db.flush()
    await db.refresh(process)

    return RAGAssessmentResponse(
        process_id=process.id,
        process_code=process.code,
        dimension=body.dimension,
        old_status=old_status,
        new_status=body.status,
        rag_overall=process.rag_overall,
        assessed_by=user.id,
        assessed_at=process.rag_last_reviewed,
    )


@router.get("/{process_id}/rag-history", response_model=RAGHistoryResponse)
async def get_rag_history(
    process_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get RAG change history for a process."""
    result = await db.execute(
        select(Process.id, Process.code).where(
            Process.id == process_id,
            Process.organization_id == user.organization_id,
        )
    )
    proc_row = result.fetchone()

    if not proc_row:
        raise HTTPException(status_code=404, detail="Process not found")

    # For now, return minimal history from audit log
    # A full implementation would query audit_logs for RAG field changes
    # This is a placeholder that returns explicit review info
    proc_result = await db.execute(
        select(Process).where(Process.id == process_id)
    )
    process = proc_result.scalar_one()

    entries = []
    if process.rag_last_reviewed:
        # Add entry for last explicit review
        entries.append(
            RAGHistoryEntry(
                timestamp=process.rag_last_reviewed,
                dimension="all",
                old_status=None,
                new_status="explicit_review",
                source="explicit_assessment",
                notes=None,
                changed_by=process.rag_reviewed_by,
            )
        )

    return RAGHistoryResponse(
        process_id=process_id,
        process_code=proc_row.code,
        entries=entries,
    )


@router.get("/rag-summary", response_model=RAGSummaryResponse)
async def get_rag_summary(
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get org-wide RAG distribution summary."""
    org_id = user.organization_id

    # Overall distribution (by rag_overall)
    overall_result = await db.execute(
        text("""
            SELECT rag_overall, COUNT(*) as count
            FROM processes
            WHERE organization_id = :org_id AND status != 'archived'
            GROUP BY rag_overall
        """),
        {"org_id": org_id},
    )
    overall = [
        RAGSummaryItem(status=row[0] or "neutral", count=row[1])
        for row in overall_result.fetchall()
    ]

    # By dimension
    by_dimension = {}
    for dim, col in DIMENSION_COLS.items():
        dim_result = await db.execute(
            text(f"""
                SELECT {col}, COUNT(*) as count
                FROM processes
                WHERE organization_id = :org_id AND status != 'archived'
                GROUP BY {col}
            """),
            {"org_id": org_id},
        )
        by_dimension[dim] = [
            RAGSummaryItem(status=row[0] or "neutral", count=row[1])
            for row in dim_result.fetchall()
        ]

    # Total processes
    total_result = await db.execute(
        select(func.count()).where(
            Process.organization_id == org_id,
            Process.status != "archived",
        )
    )
    total = total_result.scalar() or 0

    # Processes with open issues
    issues_result = await db.execute(
        select(func.count(func.distinct(IssueLog.process_id))).where(
            IssueLog.organization_id == org_id,
            IssueLog.issue_status.in_(["open", "in_progress"]),
        )
    )
    with_issues = issues_result.scalar() or 0

    return RAGSummaryResponse(
        overall_distribution=overall,
        by_dimension=by_dimension,
        total_processes=total,
        processes_with_issues=with_issues,
    )


@router.post("/rag-recalculate", response_model=RAGRecalculateResponse)
async def recalculate_rag(
    body: RAGRecalculateRequest,
    user: CurrentUser = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Admin-only: Force recalculation of RAG statuses from issue data.

    Useful after bulk issue imports or manual database corrections.
    """
    org_id = user.organization_id

    # Get target processes
    if body.process_ids:
        proc_result = await db.execute(
            select(Process.id).where(
                Process.id.in_(body.process_ids),
                Process.organization_id == org_id,
            )
        )
    else:
        proc_result = await db.execute(
            select(Process.id).where(
                Process.organization_id == org_id,
                Process.status != "archived",
            )
        )

    process_ids = [row[0] for row in proc_result.fetchall()]
    updated = 0
    errors = []

    for pid in process_ids:
        try:
            # Trigger RAG sync by doing a no-op update on any issue
            # Or call the sync function directly via raw SQL
            await db.execute(
                text("""
                    SELECT sync_process_rag_from_issues_for_process(:pid)
                """),
                {"pid": pid},
            )
            updated += 1
        except Exception as e:
            errors.append(f"Process {pid}: {str(e)}")

    # Alternative: call the trigger function for each process
    # Since we don't have a dedicated recalc function, we can create
    # a temporary issue and delete it to trigger the sync
    # For now, just update RAG based on current issue counts

    if not errors:
        # Direct recalculation without relying on trigger
        for pid in process_ids:
            await _recalculate_process_rag(db, pid)
            updated += 1

    await db.flush()

    return RAGRecalculateResponse(
        processes_updated=updated,
        errors=errors,
    )


async def _recalculate_process_rag(db: AsyncSession, process_id: str) -> None:
    """Recalculate RAG for a single process based on open issues."""
    # Get issue stats
    result = await db.execute(
        select(
            IssueLog.issue_classification,
            IssueLog.issue_criticality,
        ).where(
            IssueLog.process_id == process_id,
            IssueLog.issue_status.in_(["open", "in_progress"]),
        )
    )
    issues = result.fetchall()

    # Initialize all as neutral
    rag_values = {
        "rag_people": "neutral",
        "rag_process": "neutral",
        "rag_system": "neutral",
        "rag_data": "neutral",
    }

    # Process issues
    for classification, criticality in issues:
        col = f"rag_{classification}"
        if col in rag_values:
            if criticality == "high":
                rag_values[col] = "red"
            elif rag_values[col] != "red":
                rag_values[col] = "amber"

    # Update process
    await db.execute(
        text("""
            UPDATE processes
            SET rag_people = :rag_people,
                rag_process = :rag_process,
                rag_system = :rag_system,
                rag_data = :rag_data
            WHERE id = :pid
        """),
        {"pid": process_id, **rag_values},
    )
