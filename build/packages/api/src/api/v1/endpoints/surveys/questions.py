"""Survey question CRUD operations."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.survey import Survey, SurveyQuestion
from src.schemas.survey import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
)

router = APIRouter()


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
