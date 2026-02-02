"""
RIADA (Quality Logs) API schemas.

Blueprint §5.3.6: RIADA-to-RIADA linking (Risk → Actions, Issue → Dependencies)
"""

from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# ── Link Types ────────────────────────────────────────
RIADA_LINK_TYPES = [
    "mitigates",  # Action mitigates a Risk
    "resolves",  # Action resolves an Issue
    "blocks",  # Dependency blocks another item
    "caused_by",  # Issue caused by another item
    "related_to",  # General relationship
    "depends_on",  # Item depends on another
    "duplicates",  # Duplicate of another item
    "parent_of",  # Parent-child relationship
]


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
    tags: list[str] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RiadaListResponse(BaseModel):
    """Paginated list of RIADA items."""
    items: list[RiadaResponse]
    total: int
    page: int = 1
    per_page: int = 50
    has_more: bool = False


class RiadaSummary(BaseModel):
    """Aggregated RIADA counts for dashboard/heatmap."""
    total: int = 0
    by_type: dict[str, int] = Field(default_factory=dict)  # {risk: 5, issue: 3, ...}
    by_severity: dict[str, int] = Field(default_factory=dict)  # {critical: 1, high: 2, ...}
    by_status: dict[str, int] = Field(default_factory=dict)  # {open: 4, resolved: 2, ...}
    by_category: dict[str, int] = Field(default_factory=dict)  # {people: 2, process: 3, ...}


# ── Link Schemas ────────────────────────────────────────


class RiadaLinkCreate(BaseModel):
    """Create a link between two RIADA items."""
    target_id: str = Field(..., description="ID of the RIADA item to link to")
    link_type: str = Field(
        default="related_to",
        description="Type of relationship: mitigates, resolves, blocks, caused_by, related_to, depends_on, duplicates, parent_of"
    )
    notes: Optional[str] = Field(None, description="Optional notes about the link")


class RiadaLinkResponse(BaseModel):
    """Response for a single RIADA link."""
    id: str
    source_id: str
    target_id: str
    link_type: str
    notes: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class RiadaLinkedItemBrief(BaseModel):
    """Brief representation of a linked RIADA item."""
    id: str
    code: str
    title: str
    riada_type: str
    severity: str
    status: str
    link_id: str
    link_type: str
    link_direction: str  # "outgoing" or "incoming"


class RiadaLinksResponse(BaseModel):
    """All links for a RIADA item."""
    riada_id: str
    outgoing: list[RiadaLinkedItemBrief] = []  # Links where this item is the source
    incoming: list[RiadaLinkedItemBrief] = []  # Links where this item is the target
    total: int = 0


class RiadaDetailResponse(RiadaResponse):
    """Extended response including linked items."""
    linked_items: RiadaLinksResponse | None = None
