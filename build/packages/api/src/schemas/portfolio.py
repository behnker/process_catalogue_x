"""
Portfolio API schemas.

Blueprint §4.5: 7-level hierarchy with WSVF prioritization.
Blueprint §4.5.4: Milestones, budget tracking.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Portfolio Items ─────────────────────────────────────


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


class PortfolioItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    rag_status: Optional[str] = None
    rag_notes: Optional[str] = None
    business_value: Optional[int] = Field(None, ge=1, le=10)
    time_criticality: Optional[int] = Field(None, ge=1, le=10)
    risk_reduction: Optional[int] = Field(None, ge=1, le=10)
    job_size: Optional[int] = Field(None, ge=1, le=10)
    planned_start: Optional[date] = None
    planned_end: Optional[date] = None
    actual_start: Optional[date] = None
    actual_end: Optional[date] = None
    budget_approved: Optional[float] = None
    budget_spent: Optional[float] = None
    budget_forecast: Optional[float] = None
    owner_id: Optional[str] = None
    sponsor_id: Optional[str] = None
    sort_order: Optional[int] = None
    tags: Optional[list[str]] = None


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
    actual_start: Optional[date]
    actual_end: Optional[date]
    budget_approved: Optional[float]
    budget_spent: Optional[float]
    budget_forecast: Optional[float]
    owner_id: Optional[str]
    sponsor_id: Optional[str]
    sort_order: int
    tags: list
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PortfolioListResponse(BaseModel):
    """Paginated list of portfolio items."""
    items: list[PortfolioItemResponse]
    total: int
    page: int = 1
    per_page: int = 50
    has_more: bool = False


class PortfolioTreeNode(BaseModel):
    """Recursive tree node for portfolio hierarchy."""
    id: str
    code: str
    name: str
    level: str
    status: str
    rag_status: Optional[str]
    wsvf_score: Optional[float]
    sort_order: int
    children: list["PortfolioTreeNode"] = []

    model_config = {"from_attributes": True}


PortfolioTreeNode.model_rebuild()


# ── Milestones ──────────────────────────────────────────


class MilestoneCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    due_date: Optional[date] = None
    sort_order: int = 0


class MilestoneUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None
    status: Optional[str] = None
    sort_order: Optional[int] = None


class MilestoneResponse(BaseModel):
    id: str
    portfolio_item_id: str
    name: str
    description: Optional[str]
    due_date: Optional[date]
    completed_date: Optional[date]
    status: str
    sort_order: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
