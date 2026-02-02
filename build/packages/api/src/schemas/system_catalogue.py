"""
System Catalogue API schemas.

Blueprint §9.6.9: SystemCatalogue (25 columns), ProcessSystem (14 columns)
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Enum Value Lists (for validation) ────────────────────────

PROVIDER_TYPES = ["internal", "commercial_saas", "commercial_onprem", "custom_developed", "open_source"]
HOSTING_MODELS = ["cloud_global", "cloud_china", "on_premise", "hybrid"]
OPERATING_REGIONS = ["global", "china_only", "international_only", "multi_region"]
SYSTEM_CRITICALITIES = ["critical", "high", "medium", "low"]
LICENSE_MODELS = ["free", "subscription", "perpetual", "custom_contract", "internal"]
SYSTEM_ROLES = ["primary", "secondary", "reference", "integration_target"]
INTEGRATION_METHODS = ["api", "manual_entry", "manual_export", "file_transfer", "webhook", "central_hub"]
CATALOGUE_STATUSES = ["evaluate", "maintain", "optimize", "retire"]
PROCESS_SYSTEM_STATUSES = ["active", "planned", "deprecated"]
AUTOMATION_POTENTIALS = ["none", "low", "medium", "high"]


# ── Brief Schemas (for nested responses) ─────────────────────


class SystemBrief(BaseModel):
    """Minimal system info for nested responses."""
    id: str
    name: str
    system_type: str
    criticality: str
    status: str

    model_config = {"from_attributes": True}


class ProcessBrief(BaseModel):
    """Minimal process info for nested responses."""
    id: str
    code: str
    name: str
    level: str

    model_config = {"from_attributes": True}


# ── System Catalogue Schemas ─────────────────────────────────


class SystemCatalogueCreate(BaseModel):
    """Create a new system in the catalogue."""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    scope_description: Optional[str] = None
    system_type: str = Field(..., max_length=30)
    provider_name: Optional[str] = Field(None, max_length=255)
    provider_type: Optional[str] = Field(None, max_length=30)
    primary_users: Optional[str] = Field(None, max_length=255)
    access_methods: Optional[list[str]] = Field(default_factory=list)
    is_saas: bool = False
    hosting_model: Optional[str] = Field(None, max_length=30)
    operating_region: Optional[str] = Field(None, max_length=30)
    integration_method: Optional[str] = Field(None, max_length=255)
    criticality: str = Field(default="medium", max_length=20)
    owner_id: Optional[str] = None
    license_model: Optional[str] = Field(None, max_length=30)
    compliance_notes: Optional[str] = None
    url: Optional[str] = Field(None, max_length=500)
    status: str = Field(default="evaluate", max_length=20)
    metadata: Optional[dict] = Field(default_factory=dict)


class SystemCatalogueUpdate(BaseModel):
    """Update an existing system."""
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    scope_description: Optional[str] = None
    system_type: Optional[str] = Field(None, max_length=30)
    provider_name: Optional[str] = Field(None, max_length=255)
    provider_type: Optional[str] = Field(None, max_length=30)
    primary_users: Optional[str] = Field(None, max_length=255)
    access_methods: Optional[list[str]] = None
    is_saas: Optional[bool] = None
    hosting_model: Optional[str] = Field(None, max_length=30)
    operating_region: Optional[str] = Field(None, max_length=30)
    integration_method: Optional[str] = Field(None, max_length=255)
    criticality: Optional[str] = Field(None, max_length=20)
    owner_id: Optional[str] = None
    license_model: Optional[str] = Field(None, max_length=30)
    compliance_notes: Optional[str] = None
    url: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None, max_length=20)
    metadata: Optional[dict] = None


class SystemCatalogueResponse(BaseModel):
    """Full system response."""
    id: str
    organization_id: str
    name: str
    description: Optional[str]
    scope_description: Optional[str]
    system_type: str
    provider_name: Optional[str]
    provider_type: Optional[str]
    primary_users: Optional[str]
    access_methods: Optional[list[str]]
    is_saas: bool
    hosting_model: Optional[str]
    operating_region: Optional[str]
    integration_method: Optional[str]
    criticality: str
    owner_id: Optional[str]
    license_model: Optional[str]
    compliance_notes: Optional[str]
    url: Optional[str]
    status: str
    metadata: Optional[dict]
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str]
    updated_by: Optional[str]
    process_count: int = 0

    model_config = {"from_attributes": True}


class SystemCatalogueListResponse(BaseModel):
    """Paginated list of systems."""
    items: list[SystemCatalogueResponse]
    total: int
    page: int = 1
    per_page: int = 50
    has_more: bool = False


# ── Process-System Junction Schemas ──────────────────────────


class ProcessSystemCreate(BaseModel):
    """Create a process-system linkage (from process side - provide system_id)."""
    system_id: str
    purpose: Optional[str] = None
    system_role: str = Field(default="primary", max_length=30)
    integration_method: Optional[str] = Field(None, max_length=30)
    criticality: str = Field(default="medium", max_length=20)
    user_scope: Optional[str] = Field(None, max_length=255)
    pain_points: Optional[str] = None
    automation_potential: Optional[str] = Field(None, max_length=20)
    status: str = Field(default="active", max_length=20)


class SystemProcessCreate(BaseModel):
    """Create a process-system linkage (from system side - provide process_id)."""
    process_id: str
    purpose: Optional[str] = None
    system_role: str = Field(default="primary", max_length=30)
    integration_method: Optional[str] = Field(None, max_length=30)
    criticality: str = Field(default="medium", max_length=20)
    user_scope: Optional[str] = Field(None, max_length=255)
    pain_points: Optional[str] = None
    automation_potential: Optional[str] = Field(None, max_length=20)
    status: str = Field(default="active", max_length=20)


class ProcessSystemUpdate(BaseModel):
    """Update an existing process-system linkage."""
    purpose: Optional[str] = None
    system_role: Optional[str] = Field(None, max_length=30)
    integration_method: Optional[str] = Field(None, max_length=30)
    criticality: Optional[str] = Field(None, max_length=20)
    user_scope: Optional[str] = Field(None, max_length=255)
    pain_points: Optional[str] = None
    automation_potential: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = Field(None, max_length=20)


class ProcessSystemResponse(BaseModel):
    """Response for a process-system linkage."""
    id: str
    organization_id: str
    process_id: str
    system_id: str
    purpose: Optional[str]
    system_role: str
    integration_method: Optional[str]
    criticality: str
    user_scope: Optional[str]
    pain_points: Optional[str]
    automation_potential: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    # Nested brief objects
    system: Optional[SystemBrief] = None
    process: Optional[ProcessBrief] = None

    model_config = {"from_attributes": True}


class ProcessSystemsResponse(BaseModel):
    """List of process-system linkages."""
    items: list[ProcessSystemResponse]
    total: int
