"""RACI schemas — Create/Update/Response for process_raci rows."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProcessRaciCreate(BaseModel):
    activity: str
    responsible: Optional[str] = None
    accountable: Optional[str] = None
    consulted: Optional[str] = None
    informed: Optional[str] = None
    notes: Optional[str] = None


class ProcessRaciUpdate(BaseModel):
    activity: Optional[str] = None
    responsible: Optional[str] = None
    accountable: Optional[str] = None
    consulted: Optional[str] = None
    informed: Optional[str] = None
    notes: Optional[str] = None


class ProcessRaciResponse(BaseModel):
    id: str
    organization_id: str
    process_id: str
    activity: str
    responsible: Optional[str]
    accountable: Optional[str]
    consulted: Optional[str]
    informed: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
