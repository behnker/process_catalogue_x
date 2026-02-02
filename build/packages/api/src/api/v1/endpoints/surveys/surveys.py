"""Survey CRUD operations."""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.survey import Survey
from src.schemas.survey import (
    SurveyCreate,
    SurveyDetailResponse,
    SurveyListResponse,
    SurveyUpdate,
)

router = APIRouter()

VALID_MODES = {"ai_fluency", "operating_model", "change_readiness", "adoption_evidence"}


@router.get("/", response_model=SurveyListResponse)
async def list_surveys(
    mode: Optional[str] = Query(None),
    survey_status: Optional[str] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List surveys with optional filtering."""
    query = select(Survey).where(Survey.organization_id == user.organization_id)

    if mode:
        query = query.where(Survey.mode == mode)
    if survey_status:
        query = query.where(Survey.status == survey_status)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(Survey.created_at.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    surveys = result.scalars().all()

    return SurveyListResponse(
        items=[SurveyDetailResponse.model_validate(s) for s in surveys],
        total=total,
        page=page,
        per_page=per_page,
        has_more=(page * per_page) < total,
    )


@router.get("/{survey_id}", response_model=SurveyDetailResponse)
async def get_survey(
    survey_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get a survey with its questions."""
    result = await db.execute(
        select(Survey).where(
            Survey.id == survey_id,
            Survey.organization_id == user.organization_id,
        )
    )
    survey = result.scalar_one_or_none()

    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    return SurveyDetailResponse.model_validate(survey)


@router.post("/", response_model=SurveyDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_survey(
    body: SurveyCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new survey."""
    if body.mode not in VALID_MODES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid mode. Must be one of: {', '.join(VALID_MODES)}",
        )

    survey = Survey(
        id=str(uuid4()),
        organization_id=user.organization_id,
        **body.model_dump(),
    )
    db.add(survey)
    await db.flush()
    await db.refresh(survey)

    return SurveyDetailResponse.model_validate(survey)


@router.patch("/{survey_id}", response_model=SurveyDetailResponse)
async def update_survey(
    survey_id: str,
    body: SurveyUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a survey."""
    result = await db.execute(
        select(Survey).where(
            Survey.id == survey_id,
            Survey.organization_id == user.organization_id,
        )
    )
    survey = result.scalar_one_or_none()

    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(survey, field, value)

    await db.flush()
    await db.refresh(survey)

    return SurveyDetailResponse.model_validate(survey)


@router.delete("/{survey_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_survey(
    survey_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Archive a survey."""
    result = await db.execute(
        select(Survey).where(
            Survey.id == survey_id,
            Survey.organization_id == user.organization_id,
        )
    )
    survey = result.scalar_one_or_none()

    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    survey.status = "archived"
    await db.flush()
