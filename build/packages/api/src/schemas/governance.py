"""Governance schemas — Create/Update/Response for process_governance rows."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ProcessGovernanceCreate(BaseModel):
    forum_name: str
    cadence: Optional[str] = None
    chair: Optional[str] = None
    attendees: list[str] = Field(default_factory=list)
    decision_authority: Optional[str] = None
    escalation_path: Optional[str] = None
    approval_threshold: Optional[str] = None
    documentation: Optional[str] = None


class ProcessGovernanceUpdate(BaseModel):
    forum_name: Optional[str] = None
    cadence: Optional[str] = None
    chair: Optional[str] = None
    attendees: Optional[list[str]] = None
    decision_authority: Optional[str] = None
    escalation_path: Optional[str] = None
    approval_threshold: Optional[str] = None
    documentation: Optional[str] = None


class ProcessGovernanceResponse(BaseModel):
    id: str
    organization_id: str
    process_id: str
    forum_name: str
    cadence: Optional[str]
    chair: Optional[str]
    attendees: Optional[list[Any]]
    decision_authority: Optional[str]
    escalation_path: Optional[str]
    approval_threshold: Optional[str]
    documentation: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
