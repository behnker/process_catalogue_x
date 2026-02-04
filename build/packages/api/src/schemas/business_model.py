"""Business Model Canvas schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BusinessModelEntryCreate(BaseModel):
    component: str  # key_partners, key_activities, etc.
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    agentic_opportunity: Optional[str] = None
    agentic_readiness: Optional[str] = None


class BusinessModelEntryResponse(BaseModel):
    id: str
    component: str
    title: str
    description: Optional[str]
    sort_order: int
    agentic_opportunity: Optional[str]
    agentic_readiness: Optional[str]
    riada_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class BusinessModelCanvasResponse(BaseModel):
    """Full canvas with all 9 component groups."""
    id: str
    name: str
    entries_by_component: dict[str, list[BusinessModelEntryResponse]]
