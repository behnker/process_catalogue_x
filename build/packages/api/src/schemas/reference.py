"""
Reference Catalogue API schemas.
Departments, functions, roles, systems, clients, markets, categories, partners, suppliers.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Valid catalogue types
CATALOGUE_TYPES = [
    "departments",
    "functions",
    "roles",
    "systems",
    "clients",
    "markets",
    "categories",
    "partners",
    "suppliers",
    "tags",
]


class ReferenceCatalogueCreate(BaseModel):
    """Create a new reference catalogue entry."""
    catalogue_type: str = Field(..., description="Type: departments, functions, roles, systems, etc.")
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    parent_id: Optional[str] = None
    sort_order: Optional[int] = 0


class ReferenceCatalogueUpdate(BaseModel):
    """Update an existing reference catalogue entry."""
    code: Optional[str] = Field(None, max_length=50)
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None
    parent_id: Optional[str] = None
    sort_order: Optional[int] = None


class ReferenceCatalogueResponse(BaseModel):
    """Response for a reference catalogue entry."""
    id: str
    catalogue_type: str
    code: str
    name: str
    description: Optional[str]
    status: str
    sort_order: int
    parent_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReferenceCatalogueListResponse(BaseModel):
    """List response for reference catalogue entries."""
    items: list[ReferenceCatalogueResponse]
    total: int
