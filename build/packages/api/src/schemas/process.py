"""
Process Catalogue API schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ProcessCreate(BaseModel):
    """Create a new process. Code is auto-generated based on hierarchy."""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    level: str = Field(..., pattern="^L[0-5]$")
    parent_id: Optional[str] = None
    sort_order: Optional[int] = Field(None, description="Position hint; auto-assigned if not provided")
    process_type: str = "primary"
    status: str = "draft"
    current_automation: str = "manual"
    target_automation: Optional[str] = None
    owner_id: Optional[str] = None
    sponsor_id: Optional[str] = None
    function_id: Optional[str] = None
    tags: list[str] = []

    @field_validator("status", "process_type", "current_automation", "target_automation", mode="before")
    @classmethod
    def normalize_to_lowercase(cls, v: Optional[str]) -> Optional[str]:
        """Normalize enum-like fields to lowercase for consistent storage."""
        return v.lower() if v else v


class ProcessUpdate(BaseModel):
    """Update an existing process. Code cannot be updated directly."""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    current_automation: Optional[str] = None
    target_automation: Optional[str] = None
    automation_notes: Optional[str] = None
    owner_id: Optional[str] = None
    sponsor_id: Optional[str] = None
    tags: Optional[list[str]] = None

    @field_validator("status", "current_automation", "target_automation", mode="before")
    @classmethod
    def normalize_to_lowercase(cls, v: Optional[str]) -> Optional[str]:
        """Normalize enum-like fields to lowercase for consistent storage."""
        return v.lower() if v else v


class ProcessReorder(BaseModel):
    """Reorder a process within its hierarchy."""
    process_id: str = Field(..., description="ID of the process to reorder")
    new_sort_order: int = Field(..., ge=0, description="New position (0-based)")
    new_parent_id: Optional[str] = Field(None, description="New parent ID for reparenting")


class ProcessResponse(BaseModel):
    id: str
    code: str
    name: str
    description: Optional[str]
    level: str
    parent_id: Optional[str]
    process_type: str
    status: str
    current_automation: str
    target_automation: Optional[str]
    owner_id: Optional[str]
    sponsor_id: Optional[str]
    sort_order: int
    tags: list
    children_count: int = 0
    riada_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProcessTreeNode(BaseModel):
    """Recursive tree representation for canvas/tree views."""
    id: str
    code: str
    name: str
    level: str
    process_type: str
    status: str
    current_automation: str
    sort_order: int
    children: list["ProcessTreeNode"] = []
    riada_summary: Optional[dict] = None  # {red: 0, amber: 0, green: 0}

    model_config = {"from_attributes": True}


ProcessTreeNode.model_rebuild()


class ProcessListResponse(BaseModel):
    items: list[ProcessResponse]
    total: int
    page: int = 1
    page_size: int = 50


class OperatingModelData(BaseModel):
    component_type: str
    current_state: dict = {}
    future_state: dict = {}
    transition_notes: Optional[str] = None


class ProcessDetailResponse(ProcessResponse):
    """Extended response with operating model components."""
    operating_model: list[OperatingModelData] = []
    children: list[ProcessResponse] = []
