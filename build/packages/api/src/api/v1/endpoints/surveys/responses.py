"""Survey response submission and retrieval."""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.survey import Survey, SurveyResponse
from src.schemas.survey import (
    SurveyResponseCreate,
    SurveyResponseDetail,
    SurveyResponseSummary,
)

router = APIRouter()


@router.get("/{survey_id}/responses", response_model=list[SurveyResponseSummary])
async def list_responses(
    survey_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get all responses for a survey (summary view)."""
    result = await db.execute(
        select(SurveyResponse)
        .where(
            SurveyResponse.survey_id == survey_id,
            SurveyResponse.organization_id == user.organization_id,
        )
        .order_by(SurveyResponse.created_at.desc())
    )
    responses = result.scalars().all()
    return [SurveyResponseSummary.model_validate(r) for r in responses]


@router.get("/{survey_id}/responses/{response_id}", response_model=SurveyResponseDetail)
async def get_response(
    survey_id: str,
    response_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get a specific response with all answers."""
    result = await db.execute(
        select(SurveyResponse).where(
            SurveyResponse.id == response_id,
            SurveyResponse.survey_id == survey_id,
            SurveyResponse.organization_id == user.organization_id,
        )
    )
    response = result.scalar_one_or_none()

    if not response:
        raise HTTPException(status_code=404, detail="Response not found")

    return SurveyResponseDetail.model_validate(response)


@router.post(
    "/{survey_id}/responses",
    response_model=SurveyResponseDetail,
    status_code=status.HTTP_201_CREATED,
)
async def submit_response(
    survey_id: str,
    body: SurveyResponseCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Submit a survey response."""
    # Verify survey exists and is active
    result = await db.execute(
        select(Survey).where(
            Survey.id == survey_id,
            Survey.organization_id == user.organization_id,
        )
    )
    survey = result.scalar_one_or_none()

    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    if survey.status != "active":
        raise HTTPException(status_code=400, detail="Survey is not accepting responses")

    # Calculate score from answers if applicable
    total_score = None
    if body.answers:
        scores = [a.get("score", 0) for a in body.answers if isinstance(a, dict)]
        if scores:
            total_score = sum(scores) / len(scores) * 20  # Scale to 0-100

    response = SurveyResponse(
        id=str(uuid4()),
        organization_id=user.organization_id,
        survey_id=survey_id,
        respondent_id=user.id if not survey.is_anonymous else None,
        answers=body.answers,
        is_complete=body.is_complete,
        completed_at=datetime.now(timezone.utc) if body.is_complete else None,
        total_score=total_score,
    )
    db.add(response)
    await db.flush()
    await db.refresh(response)

    return SurveyResponseDetail.model_validate(response)
