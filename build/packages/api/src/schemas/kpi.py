"""KPI schemas — Create/Update/Response for process_kpi rows."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProcessKpiCreate(BaseModel):
    name: str
    description: Optional[str] = None
    unit: Optional[str] = None
    target_value: Optional[str] = None
    current_value: Optional[str] = None
    previous_value: Optional[str] = None
    trend: Optional[str] = None
    rag_status: Optional[str] = None
    frequency: Optional[str] = None
    data_source: Optional[str] = None
    owner_role: Optional[str] = None


class ProcessKpiUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    target_value: Optional[str] = None
    current_value: Optional[str] = None
    previous_value: Optional[str] = None
    trend: Optional[str] = None
    rag_status: Optional[str] = None
    frequency: Optional[str] = None
    data_source: Optional[str] = None
    owner_role: Optional[str] = None


class ProcessKpiResponse(BaseModel):
    id: str
    organization_id: str
    process_id: str
    name: str
    description: Optional[str]
    unit: Optional[str]
    target_value: Optional[str]
    current_value: Optional[str]
    previous_value: Optional[str]
    trend: Optional[str]
    rag_status: Optional[str]
    frequency: Optional[str]
    data_source: Optional[str]
    owner_role: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
