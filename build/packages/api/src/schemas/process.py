"""
Process Catalogue API schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProcessCreate(BaseModel):
    code: str = Field(..., max_length=20, examples=["L2-10"])
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    level: str = Field(..., pattern="^L[0-5]$")
    parent_id: Optional[str] = None
    process_type: str = "primary"
    current_automation: str = "manual"
    target_automation: Optional[str] = None
    owner_id: Optional[str] = None
    sponsor_id: Optional[str] = None
    function_id: Optional[str] = None
    tags: list[str] = []


class ProcessUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    current_automation: Optional[str] = None
    target_automation: Optional[str] = None
    automation_notes: Optional[str] = None
    owner_id: Optional[str] = None
    sponsor_id: Optional[str] = None
    sort_order: Optional[int] = None
    tags: Optional[list[str]] = None


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
