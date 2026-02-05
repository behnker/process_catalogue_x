"""Issue CRUD endpoints."""

from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.issue_log import IssueLog
from src.models.process import Process
from src.schemas.issue_log import (
    IssueCreate,
    IssueListResponse,
    IssueResponse,
    IssueUpdate,
)

router = APIRouter()

MAX_RETRY_ATTEMPTS = 3  # For issue_number race condition (CONFLICT 7)


def level_to_int(level_str: str) -> int:
    """Convert 'L0'-'L5' to 0-5."""
    return int(level_str[1]) if level_str and level_str.startswith("L") else 0


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

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Paginate
    query = query.order_by(IssueLog.issue_number.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    items = result.scalars().all()

    return IssueListResponse(
        items=[_to_response(i) for i in items],
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

    return _to_response(issue)


@router.post("/", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def create_issue(
    body: IssueCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new operational issue."""
    # Lookup process (for denormalized fields)
    proc_result = await db.execute(
        select(Process).where(
            Process.id == body.process_id,
            Process.organization_id == user.organization_id,
        )
    )
    process = proc_result.scalar_one_or_none()

    if not process:
        raise HTTPException(status_code=400, detail="Process not found")

    # Retry loop for issue_number race condition (CONFLICT 7)
    for attempt in range(MAX_RETRY_ATTEMPTS):
        try:
            issue = IssueLog(
                id=str(uuid4()),
                organization_id=user.organization_id,
                title=body.title,
                description=body.description,
                issue_classification=body.issue_classification,
                issue_criticality=body.issue_criticality,
                issue_complexity=body.issue_complexity,
                issue_status="open",
                process_id=body.process_id,
                process_level=level_to_int(process.level),
                process_ref=process.code,
                process_name=process.name,
                raised_by_id=user.id,
                assigned_to_id=body.assigned_to_id,
                date_raised=date.today(),
                target_resolution_date=body.target_resolution_date,
                opportunity_flag=body.opportunity_flag,
                opportunity_description=body.opportunity_description,
                opportunity_expected_benefit=body.opportunity_expected_benefit,
                opportunity_beneficiary_roles=body.opportunity_beneficiary_roles,
                created_by=user.id,
            )
            db.add(issue)
            await db.flush()
            await db.refresh(issue)
            return _to_response(issue)

        except IntegrityError as e:
            await db.rollback()
            if "ix_issue_log_org_number" in str(e) and attempt < MAX_RETRY_ATTEMPTS - 1:
                continue  # Retry on unique constraint violation
            raise HTTPException(
                status_code=500, detail="Failed to create issue after retries"
            )

    raise HTTPException(status_code=500, detail="Failed to create issue")


@router.patch("/{issue_id}", response_model=IssueResponse)
async def update_issue(
    issue_id: str,
    body: IssueUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update an existing issue."""
    result = await db.execute(
        select(IssueLog).where(
            IssueLog.id == issue_id,
            IssueLog.organization_id == user.organization_id,
        )
    )
    issue = result.scalar_one_or_none()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Validate status transitions (BR-01 through BR-10)
    if body.issue_status:
        _validate_status_transition(issue.issue_status, body.issue_status)

    # Apply updates
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(issue, field, value)

    issue.updated_by = user.id
    await db.flush()
    await db.refresh(issue)

    return _to_response(issue)


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(
    issue_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete an issue (only open issues can be deleted)."""
    result = await db.execute(
        select(IssueLog).where(
            IssueLog.id == issue_id,
            IssueLog.organization_id == user.organization_id,
        )
    )
    issue = result.scalar_one_or_none()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if issue.issue_status not in ("open", "deferred"):
        raise HTTPException(
            status_code=400,
            detail="Only open or deferred issues can be deleted",
        )

    await db.delete(issue)
    await db.flush()


def _validate_status_transition(current: str, new: str) -> None:
    """Validate issue status transitions per spec BR-01 through BR-10."""
    allowed = {
        "open": {"in_progress", "deferred", "closed"},
        "in_progress": {"resolved", "deferred", "open"},
        "resolved": {"closed", "in_progress"},
        "deferred": {"open", "closed"},
        "closed": set(),  # Terminal state
    }

    if new not in allowed.get(current, set()):
        raise HTTPException(
            status_code=422,
            detail=f"Cannot transition from '{current}' to '{new}'",
        )


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
