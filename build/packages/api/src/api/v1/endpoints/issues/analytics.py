"""Issue analytics endpoints — heatmap, summary, history."""

from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.issue_log import IssueLog, IssueLogHistory
from src.schemas.issue_log import (
    HeatmapCell,
    HeatmapResponse,
    IssueHistoryEntry,
    IssueHistoryResponse,
    IssueSummary,
)

router = APIRouter()


@router.get("/summary", response_model=IssueSummary)
async def get_issue_summary(
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get summary statistics for issues dashboard."""
    org_id = user.organization_id

    # Count by status
    status_counts = await db.execute(
        select(IssueLog.issue_status, func.count())
        .where(IssueLog.organization_id == org_id)
        .group_by(IssueLog.issue_status)
    )
    by_status = {row[0]: row[1] for row in status_counts.fetchall()}

    # Count by classification (open/in_progress only)
    class_counts = await db.execute(
        select(IssueLog.issue_classification, func.count())
        .where(
            IssueLog.organization_id == org_id,
            IssueLog.issue_status.in_(["open", "in_progress"]),
        )
        .group_by(IssueLog.issue_classification)
    )
    by_classification = {row[0]: row[1] for row in class_counts.fetchall()}

    # Count by criticality (open/in_progress only)
    crit_counts = await db.execute(
        select(IssueLog.issue_criticality, func.count())
        .where(
            IssueLog.organization_id == org_id,
            IssueLog.issue_status.in_(["open", "in_progress"]),
        )
        .group_by(IssueLog.issue_criticality)
    )
    by_criticality = {row[0]: row[1] for row in crit_counts.fetchall()}

    # Opportunity counts
    opp_identified = await db.execute(
        select(func.count())
        .where(
            IssueLog.organization_id == org_id,
            IssueLog.opportunity_flag == True,  # noqa: E712
        )
    )
    opp_delivered = await db.execute(
        select(func.count())
        .where(
            IssueLog.organization_id == org_id,
            IssueLog.opportunity_status == "delivered",
        )
    )

    # Overdue count
    today = date.today()
    overdue = await db.execute(
        select(func.count())
        .where(
            IssueLog.organization_id == org_id,
            IssueLog.issue_status.in_(["open", "in_progress"]),
            IssueLog.target_resolution_date < today,
        )
    )

    # Due this week
    week_end = today + timedelta(days=7)
    due_this_week = await db.execute(
        select(func.count())
        .where(
            IssueLog.organization_id == org_id,
            IssueLog.issue_status.in_(["open", "in_progress"]),
            IssueLog.target_resolution_date >= today,
            IssueLog.target_resolution_date <= week_end,
        )
    )

    return IssueSummary(
        total_open=by_status.get("open", 0),
        total_in_progress=by_status.get("in_progress", 0),
        total_resolved=by_status.get("resolved", 0),
        total_closed=by_status.get("closed", 0),
        total_deferred=by_status.get("deferred", 0),
        by_classification={
            "people": by_classification.get("people", 0),
            "process": by_classification.get("process", 0),
            "system": by_classification.get("system", 0),
            "data": by_classification.get("data", 0),
        },
        by_criticality={
            "high": by_criticality.get("high", 0),
            "medium": by_criticality.get("medium", 0),
            "low": by_criticality.get("low", 0),
        },
        opportunities_identified=opp_identified.scalar() or 0,
        opportunities_delivered=opp_delivered.scalar() or 0,
        overdue_count=overdue.scalar() or 0,
        due_this_week=due_this_week.scalar() or 0,
    )


@router.get("/heatmap", response_model=HeatmapResponse)
async def get_issue_heatmap(
    rollup: bool = Query(False, description="Include descendant issue counts"),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get process-issue heatmap data."""
    view_name = "v_process_issue_heatmap_rollup" if rollup else "v_process_issue_heatmap"

    # Note: v_process_issue_heatmap uses 'total_open_issues', rollup view uses 'total_issues'
    total_col = "total_open_issues" if not rollup else "total_issues"
    result = await db.execute(
        text(f"""
            SELECT
                process_id, process_ref, process_name, level, parent_id,
                people_count, process_count, system_count, data_count,
                people_colour, process_colour, system_colour, data_colour,
                overall_colour,
                COALESCE({total_col}, people_count + process_count + system_count + data_count) AS total_issues
            FROM {view_name}
            WHERE organization_id = :org_id
            ORDER BY process_ref
        """),
        {"org_id": user.organization_id},
    )

    cells = []
    for row in result.fetchall():
        cells.append(
            HeatmapCell(
                process_id=str(row.process_id),
                process_ref=row.process_ref,
                process_name=row.process_name,
                level=row.level,
                parent_id=str(row.parent_id) if row.parent_id else None,
                people_count=row.people_count or 0,
                process_count=row.process_count or 0,
                system_count=row.system_count or 0,
                data_count=row.data_count or 0,
                total_issues=row.total_issues or 0,
                people_colour=row.people_colour or "neutral",
                process_colour=row.process_colour or "neutral",
                system_colour=row.system_colour or "neutral",
                data_colour=row.data_colour or "neutral",
                overall_colour=row.overall_colour or "neutral",
            )
        )

    return HeatmapResponse(cells=cells, rollup=rollup)


@router.get("/{issue_id}/history", response_model=IssueHistoryResponse)
async def get_issue_history(
    issue_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get history timeline for an issue."""
    # Verify issue exists and belongs to org
    issue_result = await db.execute(
        select(IssueLog.id, IssueLog.issue_number)
        .where(
            IssueLog.id == issue_id,
            IssueLog.organization_id == user.organization_id,
        )
    )
    issue_row = issue_result.fetchone()

    if not issue_row:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Fetch history
    history_result = await db.execute(
        select(IssueLogHistory)
        .where(IssueLogHistory.issue_id == issue_id)
        .order_by(IssueLogHistory.changed_at.desc())
    )
    entries = history_result.scalars().all()

    return IssueHistoryResponse(
        issue_id=issue_id,
        display_id=f"OPS-{issue_row.issue_number:03d}",
        entries=[
            IssueHistoryEntry(
                id=e.id,
                field_name=e.field_name,
                old_value=e.old_value,
                new_value=e.new_value,
                change_note=e.change_note,
                changed_by=e.changed_by,
                changed_at=e.changed_at,
            )
            for e in entries
        ],
    )
