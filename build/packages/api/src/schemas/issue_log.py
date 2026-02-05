"""
Issue & Opportunity Log API schemas.

AMD-01: OPS- prefix for display_id (not ISS-).
AMD-02: JSONB arrays for beneficiary_roles.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class IssueCreate(BaseModel):
    """Create a new operational issue."""
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    issue_classification: str = Field(
        ..., pattern="^(people|process|system|data)$"
    )
    issue_criticality: str = Field(
        "medium", pattern="^(high|medium|low)$"
    )
    issue_complexity: str = Field(
        "medium", pattern="^(high|medium|low)$"
    )
    process_id: str = Field(..., description="UUID of linked process")
    assigned_to_id: Optional[str] = None
    target_resolution_date: Optional[date] = None

    # Opportunity fields (optional at creation)
    opportunity_flag: bool = False
    opportunity_description: Optional[str] = None
    opportunity_expected_benefit: Optional[str] = None
    opportunity_beneficiary_roles: list[str] = []

    @field_validator("issue_classification", "issue_criticality", "issue_complexity", mode="before")
    @classmethod
    def normalize_to_lowercase(cls, v: Optional[str]) -> Optional[str]:
        return v.lower() if v else v


class IssueUpdate(BaseModel):
    """Update an existing issue."""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    issue_criticality: Optional[str] = Field(
        None, pattern="^(high|medium|low)$"
    )
    issue_complexity: Optional[str] = Field(
        None, pattern="^(high|medium|low)$"
    )
    issue_status: Optional[str] = Field(
        None, pattern="^(open|in_progress|resolved|closed|deferred)$"
    )
    assigned_to_id: Optional[str] = None
    target_resolution_date: Optional[date] = None
    actual_resolution_date: Optional[date] = None
    resolution_summary: Optional[str] = None

    # Opportunity fields
    opportunity_flag: Optional[bool] = None
    opportunity_status: Optional[str] = Field(
        None, pattern="^(identified|evaluating|approved|in_delivery|delivered|rejected)$"
    )
    opportunity_description: Optional[str] = None
    opportunity_expected_benefit: Optional[str] = None
    opportunity_beneficiary_roles: Optional[list[str]] = None

    @field_validator("issue_criticality", "issue_complexity", "issue_status", "opportunity_status", mode="before")
    @classmethod
    def normalize_to_lowercase(cls, v: Optional[str]) -> Optional[str]:
        return v.lower() if v else v


class IssueResponse(BaseModel):
    """Single issue response."""
    id: str
    display_id: str  # AMD-01: OPS-001 format
    issue_number: int
    title: str
    description: Optional[str]
    issue_classification: str
    issue_criticality: str
    issue_complexity: str
    issue_status: str

    # Process linkage (denormalized)
    process_id: str
    process_level: int
    process_ref: str
    process_name: str

    # Ownership
    raised_by_id: str
    assigned_to_id: Optional[str]

    # Dates
    date_raised: date
    target_resolution_date: Optional[date]
    actual_resolution_date: Optional[date]

    # Resolution
    resolution_summary: Optional[str]

    # Opportunity
    opportunity_flag: bool
    opportunity_status: Optional[str]
    opportunity_description: Optional[str]
    opportunity_expected_benefit: Optional[str]
    opportunity_beneficiary_roles: list[str] = []

    # Audit
    created_by: str
    updated_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class IssueListResponse(BaseModel):
    """Paginated issue list."""
    items: list[IssueResponse]
    total: int = Field(..., ge=0)
    page: int = Field(1, ge=1)
    per_page: int = Field(50, ge=1, le=100)
    has_more: bool = False


class IssueHistoryEntry(BaseModel):
    """Single history entry."""
    id: str
    field_name: str
    old_value: Optional[str]
    new_value: Optional[str]
    change_note: Optional[str]
    changed_by: str
    changed_at: datetime

    model_config = {"from_attributes": True}


class IssueHistoryResponse(BaseModel):
    """Issue history timeline."""
    issue_id: str
    display_id: str
    entries: list[IssueHistoryEntry]


class IssueSummary(BaseModel):
    """Summary statistics for issues dashboard."""
    total_open: int
    total_in_progress: int
    total_resolved: int
    total_closed: int
    total_deferred: int

    by_classification: dict[str, int]  # people, process, system, data
    by_criticality: dict[str, int]     # high, medium, low

    opportunities_identified: int
    opportunities_delivered: int

    overdue_count: int
    due_this_week: int


class HeatmapCell(BaseModel):
    """Single cell in the process-issue heatmap."""
    process_id: str
    process_ref: str
    process_name: str
    level: str
    parent_id: Optional[str]

    # Issue counts by classification
    people_count: int
    process_count: int
    system_count: int
    data_count: int
    total_issues: int

    # Colour per addendum: high=red, any=amber, none=neutral
    people_colour: str
    process_colour: str
    system_colour: str
    data_colour: str
    overall_colour: str


class HeatmapResponse(BaseModel):
    """Process-issue heatmap data."""
    cells: list[HeatmapCell]
    rollup: bool = False  # True if includes descendant rollup


class IssueExportRequest(BaseModel):
    """Export request parameters."""
    format: str = Field("csv", pattern="^(csv|xlsx)$")
    status_filter: Optional[list[str]] = None
    classification_filter: Optional[list[str]] = None
    criticality_filter: Optional[list[str]] = None
    process_ids: Optional[list[str]] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
