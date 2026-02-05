"""
RAG Assessment API schemas.

Per RAG_Issue_Alignment_Addendum.docx:
- BR-12: GREEN requires explicit assessment with no open issues
- BR-13: NEUTRAL is default
- BR-14: Overall follows weakest-link rule
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class RAGAssessmentRequest(BaseModel):
    """Request to set explicit RAG assessment for a process dimension."""
    dimension: str = Field(
        ..., pattern="^(people|process|system|data)$",
        description="Which dimension to assess"
    )
    status: str = Field(
        ..., pattern="^(red|amber|green|neutral)$",
        description="New RAG status"
    )
    notes: Optional[str] = Field(
        None, description="Assessment rationale"
    )

    @field_validator("dimension", "status", mode="before")
    @classmethod
    def normalize_to_lowercase(cls, v: Optional[str]) -> Optional[str]:
        return v.lower() if v else v


class RAGAssessmentResponse(BaseModel):
    """Response after RAG assessment."""
    process_id: str
    process_code: str
    dimension: str
    old_status: str
    new_status: str
    rag_overall: str
    assessed_by: str
    assessed_at: datetime


class RAGConflictError(BaseModel):
    """Returned when GREEN is blocked by open issues."""
    error: str = "Cannot set GREEN with open issues"
    dimension: str
    open_issue_count: int
    open_issue_ids: list[str]


class RAGHistoryEntry(BaseModel):
    """Single RAG history entry."""
    timestamp: datetime
    dimension: str
    old_status: Optional[str]
    new_status: str
    source: str  # "issue_sync" or "explicit_assessment"
    notes: Optional[str]
    changed_by: Optional[str]


class RAGHistoryResponse(BaseModel):
    """RAG change history for a process."""
    process_id: str
    process_code: str
    entries: list[RAGHistoryEntry]


class RAGSummaryItem(BaseModel):
    """RAG status count for summary."""
    status: str
    count: int


class RAGSummaryResponse(BaseModel):
    """Org-wide RAG distribution summary."""
    overall_distribution: list[RAGSummaryItem]
    by_dimension: dict[str, list[RAGSummaryItem]]
    total_processes: int
    processes_with_issues: int


class RAGRecalculateRequest(BaseModel):
    """Request to recalculate RAG statuses (admin only)."""
    process_ids: Optional[list[str]] = Field(
        None, description="Specific processes, or None for all"
    )


class RAGRecalculateResponse(BaseModel):
    """Result of RAG recalculation."""
    processes_updated: int
    errors: list[str] = []
