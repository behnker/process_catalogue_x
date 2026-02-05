"""Issue read endpoints (list, get)."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.issue_log import IssueLog
from src.schemas.issue_log import IssueListResponse, IssueResponse

from .helpers import to_response

router = APIRouter()


@router.get("/", response_model=IssueListResponse)
async def list_issues(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    status_filter: str | None = Query(None, description="Comma-separated statuses"),
    classification: str | None = Query(None),
    criticality: str | None = Query(None),
    process_id: str | None = Query(None),
    assigned_to: str | None = Query(None),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List issues with filtering and pagination."""
    query = select(IssueLog).where(
        IssueLog.organization_id == user.organization_id
    )

    if status_filter:
        statuses = [s.strip() for s in status_filter.split(",")]
        query = query.where(IssueLog.issue_status.in_(statuses))
    if classification:
        query = query.where(IssueLog.issue_classification == classification.lower())
    if criticality:
        query = query.where(IssueLog.issue_criticality == criticality.lower())
    if process_id:
        query = query.where(IssueLog.process_id == process_id)
    if assigned_to:
        query = query.where(IssueLog.assigned_to_id == assigned_to)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(IssueLog.issue_number.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    items = result.scalars().all()

    return IssueListResponse(
        items=[to_response(i) for i in items],
        total=total,
        page=page,
        per_page=per_page,
        has_more=(page * per_page) < total,
    )


@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(
    issue_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get a single issue by ID."""
    result = await db.execute(
        select(IssueLog).where(
            IssueLog.id == issue_id,
            IssueLog.organization_id == user.organization_id,
        )
    )
    issue = result.scalar_one_or_none()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    return to_response(issue)
