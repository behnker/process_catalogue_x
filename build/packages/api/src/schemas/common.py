"""
Additional API schemas: Portfolio, Business Model, Survey, Reference Data.
Common schemas for pagination, errors, etc.
"""

from datetime import date, datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field, field_validator


T = TypeVar("T")


# ── Portfolio ────────────────────────────────────────

class PortfolioItemCreate(BaseModel):
    code: str = Field(..., max_length=30)
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    level: str  # strategy, portfolio, programme, project, workstream, epic, task
    parent_id: Optional[str] = None
    status: str = "proposed"
    business_value: Optional[int] = Field(None, ge=1, le=10)
    time_criticality: Optional[int] = Field(None, ge=1, le=10)
    risk_reduction: Optional[int] = Field(None, ge=1, le=10)
    job_size: Optional[int] = Field(None, ge=1, le=10)
    planned_start: Optional[date] = None
    planned_end: Optional[date] = None
    budget_approved: Optional[float] = None
    owner_id: Optional[str] = None
    sponsor_id: Optional[str] = None
    linked_process_ids: list[str] = []
    tags: list[str] = []


class PortfolioItemResponse(BaseModel):
    id: str
    code: str
    name: str
    description: Optional[str]
    level: str
    parent_id: Optional[str]
    status: str
    rag_status: Optional[str]
    wsvf_score: Optional[float]
    planned_start: Optional[date]
    planned_end: Optional[date]
    budget_approved: Optional[float]
    budget_spent: Optional[float]
    owner_id: Optional[str]
    tags: list[str] = []
    children_count: int = 0
    riada_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PortfolioListResponse(BaseModel):
    """Paginated list of portfolio items."""
    items: list[PortfolioItemResponse]
    total: int = Field(..., ge=0)
    page: int = Field(1, ge=1)
    per_page: int = Field(50, ge=1, le=100)
    has_more: bool = False


# ── Business Model ───────────────────────────────────

class BusinessModelEntryCreate(BaseModel):
    component: str  # key_partners, key_activities, etc.
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    agentic_opportunity: Optional[str] = None
    agentic_readiness: Optional[str] = None


class BusinessModelEntryResponse(BaseModel):
    id: str
    component: str
    title: str
    description: Optional[str]
    sort_order: int
    agentic_opportunity: Optional[str]
    agentic_readiness: Optional[str]
    riada_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class BusinessModelCanvasResponse(BaseModel):
    """Full canvas with all 9 component groups."""
    id: str
    name: str
    entries_by_component: dict[str, list[BusinessModelEntryResponse]]


# ── Survey ───────────────────────────────────────────

class SurveyCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    mode: str  # ai_fluency, operating_model, change_readiness, adoption_evidence
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_anonymous: bool = False


class SurveyResponse_(BaseModel):  # trailing underscore to avoid name collision
    id: str
    title: str
    description: Optional[str]
    mode: str
    status: str
    start_date: Optional[date]
    end_date: Optional[date]
    question_count: int = 0
    response_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Reference Data ───────────────────────────────────

class ReferenceCatalogueCreate(BaseModel):
    catalogue_type: str
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=255)
    description: Optional[str] = None


class ReferenceCatalogueResponse(BaseModel):
    id: str
    catalogue_type: str
    code: str
    name: str
    description: Optional[str]
    status: str
    sort_order: int

    model_config = {"from_attributes": True}


# ── Common ───────────────────────────────────────────

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standard paginated response format.

    Matches frontend PaginatedResponse<T> interface.
    """
    items: list[T]
    total: int = Field(..., ge=0, description="Total number of items across all pages")
    page: int = Field(1, ge=1, description="Current page number (1-indexed)")
    per_page: int = Field(50, ge=1, le=100, description="Items per page")
    has_more: bool = Field(..., description="Whether more pages exist")

    @field_validator("has_more", mode="before")
    @classmethod
    def compute_has_more(cls, v, info):
        """Auto-compute has_more if not provided."""
        if v is not None:
            return v
        total = info.data.get("total", 0)
        page = info.data.get("page", 1)
        per_page = info.data.get("per_page", 50)
        return (page * per_page) < total

    @property
    def total_pages(self) -> int:
        """Calculate total pages."""
        if self.per_page <= 0:
            return 0
        return (self.total + self.per_page - 1) // self.per_page


class ErrorDetail(BaseModel):
    """Detail about a specific error."""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None


class ErrorResponse(BaseModel):
    """
    Standard error response format.

    Consistent format across all endpoints for error handling.
    """
    error: dict[str, Any] = Field(
        ...,
        description="Error details",
        examples=[{
            "code": "VALIDATION_ERROR",
            "message": "Invalid input data",
            "details": [{"field": "name", "message": "Name is required"}]
        }]
    )

    @classmethod
    def create(
        cls,
        code: str,
        message: str,
        details: Optional[list[dict[str, Any]]] = None
    ) -> "ErrorResponse":
        """Factory method to create an error response."""
        return cls(
            error={
                "code": code,
                "message": message,
                "details": details or []
            }
        )


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str
    environment: str
