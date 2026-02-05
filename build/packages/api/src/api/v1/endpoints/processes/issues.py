"""Process-specific issue endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.issue_log import IssueLog
from src.models.process import Process
from src.schemas.issue_log import IssueListResponse, IssueResponse

router = APIRouter()


@router.get("/{process_id}/issues", response_model=IssueListResponse)
async def get_process_issues(
    process_id: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    status_filter: str | None = Query(None, description="Comma-separated statuses"),
    include_descendants: bool = Query(
        False, description="Include issues from child processes"
    ),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get issues linked to a specific process."""
    # Verify process exists
    proc_result = await db.execute(
        select(Process.id)
        .where(
            Process.id == process_id,
            Process.organization_id == user.organization_id,
        )
    )
    if not proc_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Process not found")

    # Build process ID list
    process_ids = [process_id]

    if include_descendants:
        # Get all descendant process IDs recursively
        descendant_ids = await _get_descendant_ids(db, user.organization_id, process_id)
        process_ids.extend(descendant_ids)

    # Query issues
    query = select(IssueLog).where(
        IssueLog.organization_id == user.organization_id,
        IssueLog.process_id.in_(process_ids),
    )

    if status_filter:
        statuses = [s.strip() for s in status_filter.split(",")]
        query = query.where(IssueLog.issue_status.in_(statuses))

    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Paginate
    query = query.order_by(IssueLog.issue_number.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    issues = result.scalars().all()

    return IssueListResponse(
        items=[_to_response(i) for i in issues],
        total=total,
        page=page,
        per_page=per_page,
        has_more=(page * per_page) < total,
    )


async def _get_descendant_ids(
    db: AsyncSession, org_id: str, parent_id: str
) -> list[str]:
    """Recursively get all descendant process IDs."""
    descendants = []

    result = await db.execute(
        select(Process.id).where(
            Process.organization_id == org_id,
            Process.parent_id == parent_id,
            Process.status != "archived",
        )
    )
    child_ids = [row[0] for row in result.fetchall()]

    for child_id in child_ids:
        descendants.append(child_id)
        descendants.extend(await _get_descendant_ids(db, org_id, child_id))

    return descendants


def _to_response(issue: IssueLog) -> IssueResponse:
    """Convert IssueLog model to response schema."""
    return IssueResponse(
        id=issue.id,
        display_id=issue.display_id,
        issue_number=issue.issue_number,
        title=issue.title,
        description=issue.description,
        issue_classification=issue.issue_classification,
        issue_criticality=issue.issue_criticality,
        issue_complexity=issue.issue_complexity,
        issue_status=issue.issue_status,
        process_id=issue.process_id,
        process_level=issue.process_level,
        process_ref=issue.process_ref,
        process_name=issue.process_name,
        raised_by_id=issue.raised_by_id,
        assigned_to_id=issue.assigned_to_id,
        date_raised=issue.date_raised,
        target_resolution_date=issue.target_resolution_date,
        actual_resolution_date=issue.actual_resolution_date,
        resolution_summary=issue.resolution_summary,
        opportunity_flag=issue.opportunity_flag,
        opportunity_status=issue.opportunity_status,
        opportunity_description=issue.opportunity_description,
        opportunity_expected_benefit=issue.opportunity_expected_benefit,
        opportunity_beneficiary_roles=issue.opportunity_beneficiary_roles or [],
        created_by=issue.created_by,
        updated_by=issue.updated_by,
        created_at=issue.created_at,
        updated_at=issue.updated_at,
    )
