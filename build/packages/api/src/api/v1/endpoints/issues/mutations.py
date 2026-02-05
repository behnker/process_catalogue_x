"""Issue write endpoints (create, update, delete)."""

from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.issue_log import IssueLog
from src.models.process import Process
from src.schemas.issue_log import IssueCreate, IssueResponse, IssueUpdate

from .helpers import level_to_int, to_response, validate_status_transition

router = APIRouter()

MAX_RETRY_ATTEMPTS = 3  # For issue_number race condition (CONFLICT 7)


@router.post("/", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def create_issue(
    body: IssueCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new operational issue."""
    proc_result = await db.execute(
        select(Process).where(
            Process.id == body.process_id,
            Process.organization_id == user.organization_id,
        )
    )
    process = proc_result.scalar_one_or_none()

    if not process:
        raise HTTPException(status_code=400, detail="Process not found")

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
            return to_response(issue)

        except IntegrityError as e:
            await db.rollback()
            if "ix_issue_log_org_number" in str(e) and attempt < MAX_RETRY_ATTEMPTS - 1:
                continue
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

    if body.issue_status:
        validate_status_transition(issue.issue_status, body.issue_status)

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(issue, field, value)

    issue.updated_by = user.id
    await db.flush()
    await db.refresh(issue)

    return to_response(issue)


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
