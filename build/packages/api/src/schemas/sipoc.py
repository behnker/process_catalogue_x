"""SIPOC schemas — Create/Update/Response for process_sipoc rows."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProcessSipocCreate(BaseModel):
    element_type: str  # supplier, input, output, customer
    name: str
    description: Optional[str] = None
    sort_order: int = 0


class ProcessSipocUpdate(BaseModel):
    element_type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None


class ProcessSipocResponse(BaseModel):
    id: str
    organization_id: str
    process_id: str
    element_type: str
    name: str
    description: Optional[str]
    sort_order: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
