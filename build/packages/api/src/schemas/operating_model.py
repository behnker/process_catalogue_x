"""
Operating Model API schemas.

Blueprint §4.4.1: 10 components with current/future state.
JSONB schemas for resources, security, data components.
Summary schema aggregates relational + JSONB sources.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class OperatingModelComponentCreate(BaseModel):
    component_type: str  # resources, security, data (JSONB-only)
    current_state: dict[str, Any] = Field(default_factory=dict)
    future_state: dict[str, Any] = Field(default_factory=dict)
    transition_notes: Optional[str] = None


class OperatingModelComponentUpdate(BaseModel):
    current_state: Optional[dict[str, Any]] = None
    future_state: Optional[dict[str, Any]] = None
    transition_notes: Optional[str] = None


class OperatingModelComponentResponse(BaseModel):
    id: str
    process_id: str
    component_type: str
    current_state: dict
    future_state: dict
    transition_notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OperatingModelSummary(BaseModel):
    """Summary of operating model completeness for a process."""
    process_id: str
    total_components: int
    defined_components: list[str]
    missing_components: list[str]
    components_with_gaps: list[str]
    completion_percentage: int


class RoleCatalogueCreate(BaseModel):
    name: str
    scope: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0


class RoleCatalogueUpdate(BaseModel):
    name: Optional[str] = None
    scope: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class RoleCatalogueResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    scope: Optional[str]
    description: Optional[str]
    is_active: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
