"""Policy schemas — Create/Update/Response for process_policy rows."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class ProcessPolicyCreate(BaseModel):
    name: str
    policy_type: str
    description: Optional[str] = None
    compliance_requirement: Optional[str] = None
    owner_role: Optional[str] = None
    last_reviewed: Optional[date] = None
    is_active: bool = True


class ProcessPolicyUpdate(BaseModel):
    name: Optional[str] = None
    policy_type: Optional[str] = None
    description: Optional[str] = None
    compliance_requirement: Optional[str] = None
    owner_role: Optional[str] = None
    last_reviewed: Optional[date] = None
    is_active: Optional[bool] = None


class ProcessPolicyResponse(BaseModel):
    id: str
    organization_id: str
    process_id: str
    name: str
    policy_type: str
    description: Optional[str]
    compliance_requirement: Optional[str]
    owner_role: Optional[str]
    last_reviewed: Optional[date]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
