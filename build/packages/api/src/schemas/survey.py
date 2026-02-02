"""
Survey API schemas.

Blueprint §4.7: 4 survey modes with question types and scoring.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Surveys ─────────────────────────────────────────────


class SurveyCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    mode: str  # ai_fluency, operating_model, change_readiness, adoption_evidence
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_anonymous: bool = False
    linked_process_ids: list[str] = []


class SurveyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_anonymous: Optional[bool] = None


class SurveyDetailResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    mode: str
    status: str
    start_date: Optional[date]
    end_date: Optional[date]
    is_anonymous: bool
    question_count: int = 0
    response_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SurveyListResponse(BaseModel):
    items: list[SurveyDetailResponse]
    total: int
    page: int = 1
    page_size: int = 50


# ── Questions ───────────────────────────────────────────


class QuestionCreate(BaseModel):
    question_text: str
    question_type: str  # likert_5, likert_7, multiple_choice, single_choice, text, rating, yes_no, matrix
    is_required: bool = True
    sort_order: int = 0
    options: list = []  # For choice-based questions
    scoring_weight: float = 1.0
    conditions: Optional[dict] = None  # Branching logic


class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    is_required: Optional[bool] = None
    sort_order: Optional[int] = None
    options: Optional[list] = None
    scoring_weight: Optional[float] = None
    conditions: Optional[dict] = None


class QuestionResponse(BaseModel):
    id: str
    survey_id: str
    question_text: str
    question_type: str
    is_required: bool
    sort_order: int
    options: list
    scoring_weight: float
    conditions: Optional[dict]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Responses ───────────────────────────────────────────


class SurveyResponseCreate(BaseModel):
    answers: list[dict] = []  # [{question_id: "...", value: ..., score: ...}]
    is_complete: bool = False


class SurveyResponseSummary(BaseModel):
    id: str
    survey_id: str
    respondent_id: Optional[str]
    is_complete: bool
    completed_at: Optional[datetime]
    total_score: Optional[float]
    created_at: datetime

    model_config = {"from_attributes": True}


class SurveyResponseDetail(BaseModel):
    id: str
    survey_id: str
    respondent_id: Optional[str]
    answers: list
    is_complete: bool
    completed_at: Optional[datetime]
    total_score: Optional[float]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
