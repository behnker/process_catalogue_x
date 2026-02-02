"""
Operating Model API schemas.

Blueprint §4.4.1: 10 components with current/future state.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from typing import Any


class OperatingModelComponentCreate(BaseModel):
    component_type: str  # sipoc, raci, kpis, systems, policies, timing, governance, security, data, resources
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
