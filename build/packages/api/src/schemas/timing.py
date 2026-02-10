"""Timing schemas — Create/Update/Response for process_timing rows."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProcessTimingCreate(BaseModel):
    name: str
    frequency: Optional[str] = None
    volume_per_period: Optional[str] = None
    cycle_time_target: Optional[str] = None
    cycle_time_actual: Optional[str] = None
    sla_commitment: Optional[str] = None
    trigger_event: Optional[str] = None
    dependencies: Optional[str] = None
    peak_season: Optional[str] = None


class ProcessTimingUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[str] = None
    volume_per_period: Optional[str] = None
    cycle_time_target: Optional[str] = None
    cycle_time_actual: Optional[str] = None
    sla_commitment: Optional[str] = None
    trigger_event: Optional[str] = None
    dependencies: Optional[str] = None
    peak_season: Optional[str] = None


class ProcessTimingResponse(BaseModel):
    id: str
    organization_id: str
    process_id: str
    name: str
    frequency: Optional[str]
    volume_per_period: Optional[str]
    cycle_time_target: Optional[str]
    cycle_time_actual: Optional[str]
    sla_commitment: Optional[str]
    trigger_event: Optional[str]
    dependencies: Optional[str]
    peak_season: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
