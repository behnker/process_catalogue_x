"""
Survey API endpoints.
Full CRUD for surveys, questions, and responses.

Blueprint §4.7: 4 survey modes:
  - ai_fluency: AI Fluency Survey (AFI score 0-100)
  - operating_model: Operating Model Survey (SPRD x RAG)
  - change_readiness: Change Readiness Survey (ADKAR-based)
  - adoption_evidence: Adoption Evidence Survey
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.survey import Survey, SurveyQuestion, SurveyResponse
from src.schemas.survey import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
    SurveyCreate,
    SurveyDetailResponse,
    SurveyListResponse,
    SurveyResponseCreate,
    SurveyResponseDetail,
    SurveyResponseSummary,
    SurveyUpdate,
)

router = APIRouter()

VALID_MODES = {"ai_fluency", "operating_model", "change_readiness", "adoption_evidence"}


# ── Surveys ─────────────────────────────────────────────


@router.get("/", response_model=SurveyListResponse)
async def list_surveys(
    mode: Optional[str] = Query(None),
    survey_status: Optional[str] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
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
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    surveys = result.scalars().all()

    return SurveyListResponse(
        items=[SurveyDetailResponse.model_validate(s) for s in surveys],
        total=total,
        page=page,
        page_size=page_size,
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


# ── Questions ───────────────────────────────────────────


@router.get("/{survey_id}/questions", response_model=list[QuestionResponse])
async def list_questions(
    survey_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get all questions for a survey."""
    result = await db.execute(
        select(SurveyQuestion)
        .where(
            SurveyQuestion.survey_id == survey_id,
            SurveyQuestion.organization_id == user.organization_id,
        )
        .order_by(SurveyQuestion.sort_order)
    )
    questions = result.scalars().all()
    return [QuestionResponse.model_validate(q) for q in questions]


@router.post(
    "/{survey_id}/questions",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_question(
    survey_id: str,
    body: QuestionCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Add a question to a survey."""
    # Verify survey exists
    result = await db.execute(
        select(Survey).where(
            Survey.id == survey_id,
            Survey.organization_id == user.organization_id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Survey not found")

    question = SurveyQuestion(
        id=str(uuid4()),
        organization_id=user.organization_id,
        survey_id=survey_id,
        **body.model_dump(),
    )
    db.add(question)
    await db.flush()
    await db.refresh(question)

    return QuestionResponse.model_validate(question)


@router.patch("/{survey_id}/questions/{question_id}", response_model=QuestionResponse)
async def update_question(
    survey_id: str,
    question_id: str,
    body: QuestionUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a question."""
    result = await db.execute(
        select(SurveyQuestion).where(
            SurveyQuestion.id == question_id,
            SurveyQuestion.survey_id == survey_id,
            SurveyQuestion.organization_id == user.organization_id,
        )
    )
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(question, field, value)

    await db.flush()
    await db.refresh(question)

    return QuestionResponse.model_validate(question)


@router.delete(
    "/{survey_id}/questions/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_question(
    survey_id: str,
    question_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a question."""
    result = await db.execute(
        select(SurveyQuestion).where(
            SurveyQuestion.id == question_id,
            SurveyQuestion.survey_id == survey_id,
            SurveyQuestion.organization_id == user.organization_id,
        )
    )
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    await db.delete(question)
    await db.flush()


# ── Responses ───────────────────────────────────────────


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
