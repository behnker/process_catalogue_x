"""
RIADA (Quality Logs) API schemas.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class RiadaCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    riada_type: str  # risk, issue, action, dependency, assumption
    category: str  # people, process, system, data
    severity: str = "medium"
    probability: Optional[int] = Field(None, ge=1, le=5)
    impact: Optional[int] = Field(None, ge=1, le=5)
    mitigation_plan: Optional[str] = None
    due_date: Optional[date] = None
    assigned_to_id: Optional[str] = None
    process_id: Optional[str] = None
    portfolio_item_id: Optional[str] = None
    business_model_entry_id: Optional[str] = None
    tags: list[str] = []


class RiadaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    probability: Optional[int] = Field(None, ge=1, le=5)
    impact: Optional[int] = Field(None, ge=1, le=5)
    mitigation_plan: Optional[str] = None
    due_date: Optional[date] = None
    assigned_to_id: Optional[str] = None
    rag_status: Optional[str] = None
    resolution_notes: Optional[str] = None
    tags: Optional[list[str]] = None


class RiadaResponse(BaseModel):
    id: str
    code: str
    title: str
    description: Optional[str]
    riada_type: str
    category: str
    severity: str
    status: str
    probability: Optional[int]
    impact: Optional[int]
    risk_score: Optional[int]
    mitigation_plan: Optional[str]
    due_date: Optional[date]
    assigned_to_id: Optional[str]
    raised_by_id: Optional[str]
    process_id: Optional[str]
    portfolio_item_id: Optional[str]
    business_model_entry_id: Optional[str]
    rag_status: Optional[str]
    resolution_notes: Optional[str]
    tags: list
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RiadaListResponse(BaseModel):
    items: list[RiadaResponse]
    total: int
    page: int = 1
    page_size: int = 50


class RiadaSummary(BaseModel):
    """Aggregated RIADA counts for dashboard/heatmap."""
    total: int = 0
    by_type: dict = {}  # {risk: 5, issue: 3, ...}
    by_severity: dict = {}  # {critical: 1, high: 2, ...}
    by_status: dict = {}  # {open: 4, resolved: 2, ...}
    by_category: dict = {}  # {people: 2, process: 3, ...}
