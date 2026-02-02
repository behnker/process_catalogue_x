"""
Survey models.

Blueprint §4.7: 4 survey modes:
  Mode 1: AI Fluency Survey
  Mode 2: Operating Model Survey
  Mode 3: Change Readiness Survey
  Mode 4: Adoption Evidence Survey

Blueprint §4.7.6: Survey builder with question types, scoring, branching.
Blueprint §4.7.8: Survey data model.
"""

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel

import enum


class SurveyMode(str, enum.Enum):
    AI_FLUENCY = "ai_fluency"
    OPERATING_MODEL = "operating_model"
    CHANGE_READINESS = "change_readiness"
    ADOPTION_EVIDENCE = "adoption_evidence"


class SurveyStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"


class QuestionType(str, enum.Enum):
    LIKERT_5 = "likert_5"
    LIKERT_7 = "likert_7"
    MULTIPLE_CHOICE = "multiple_choice"
    SINGLE_CHOICE = "single_choice"
    TEXT = "text"
    RATING = "rating"
    YES_NO = "yes_no"
    MATRIX = "matrix"


class Survey(TenantModel):
    """A survey template that can be deployed to users."""

    __tablename__ = "surveys"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    mode: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default=SurveyStatus.DRAFT.value)

    # Deployment
    target_audience: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)

    # Process linkage (optional — ties survey to specific processes)
    linked_process_ids: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    # Relationships
    questions: Mapped[list["SurveyQuestion"]] = relationship(
        back_populates="survey", lazy="selectin", order_by="SurveyQuestion.sort_order"
    )
    responses: Mapped[list["SurveyResponse"]] = relationship(
        back_populates="survey", lazy="noload"
    )


class SurveyQuestion(TenantModel):
    """Individual question within a survey."""

    __tablename__ = "survey_questions"

    survey_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("surveys.id"), nullable=False, index=True
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(30), nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # Options for choice-based questions
    options: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    # Scoring (for likert/rating questions)
    scoring_weight: Mapped[Optional[float]] = mapped_column(default=1.0)

    # Conditional logic (branching)
    conditions: Mapped[Optional[dict]] = mapped_column(JSONB)

    survey: Mapped["Survey"] = relationship(back_populates="questions")


class SurveyResponse(TenantModel):
    """A user's complete response to a survey deployment."""

    __tablename__ = "survey_responses"

    survey_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("surveys.id"), nullable=False, index=True
    )
    respondent_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    total_score: Mapped[Optional[float]] = mapped_column()

    # Individual answers stored as JSONB array
    answers: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    survey: Mapped["Survey"] = relationship(back_populates="responses")
