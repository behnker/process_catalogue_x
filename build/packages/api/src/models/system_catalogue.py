"""
System Catalogue models — dedicated system registry.

Blueprint §9.6.9: System Catalogue replaces generic reference_catalogues
for systems with a purpose-built schema supporting Surity's 8 registered systems.
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel

import enum


# ── Enum Definitions ─────────────────────────────────────────


class ProviderType(str, enum.Enum):
    INTERNAL = "internal"
    COMMERCIAL_SAAS = "commercial_saas"
    COMMERCIAL_ONPREM = "commercial_onprem"
    CUSTOM_DEVELOPED = "custom_developed"
    OPEN_SOURCE = "open_source"


class HostingModel(str, enum.Enum):
    CLOUD_GLOBAL = "cloud_global"
    CLOUD_CHINA = "cloud_china"
    ON_PREMISE = "on_premise"
    HYBRID = "hybrid"


class OperatingRegion(str, enum.Enum):
    GLOBAL = "global"
    CHINA_ONLY = "china_only"
    INTERNATIONAL_ONLY = "international_only"
    MULTI_REGION = "multi_region"


class SystemCriticality(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class LicenseModel(str, enum.Enum):
    FREE = "free"
    SUBSCRIPTION = "subscription"
    PERPETUAL = "perpetual"
    CUSTOM_CONTRACT = "custom_contract"
    INTERNAL = "internal"


class SystemRole(str, enum.Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    REFERENCE = "reference"
    INTEGRATION_TARGET = "integration_target"


class IntegrationMethod(str, enum.Enum):
    API = "api"
    MANUAL_ENTRY = "manual_entry"
    MANUAL_EXPORT = "manual_export"
    FILE_TRANSFER = "file_transfer"
    WEBHOOK = "webhook"
    CENTRAL_HUB = "central_hub"


class CatalogueStatus(str, enum.Enum):
    EVALUATE = "evaluate"
    MAINTAIN = "maintain"
    OPTIMIZE = "optimize"
    RETIRE = "retire"


class ProcessSystemStatus(str, enum.Enum):
    ACTIVE = "active"
    PLANNED = "planned"
    DEPRECATED = "deprecated"


class AutomationPotential(str, enum.Enum):
    """Reused from process model concept."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ── Models ───────────────────────────────────────────────────


class SystemCatalogue(TenantModel):
    """
    Dedicated system registry with 25 columns.
    Replaces generic reference_catalogues for systems.
    """

    __tablename__ = "system_catalogue"

    # ── Core Identity ────────────────────────────────
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    scope_description: Mapped[Optional[str]] = mapped_column(Text)
    system_type: Mapped[str] = mapped_column(String(30), nullable=False)

    # ── Provider Info ────────────────────────────────
    provider_name: Mapped[Optional[str]] = mapped_column(String(255))
    provider_type: Mapped[Optional[str]] = mapped_column(String(30))

    # ── Usage ────────────────────────────────────────
    primary_users: Mapped[Optional[str]] = mapped_column(String(255))
    access_methods: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    # ── Infrastructure ───────────────────────────────
    is_saas: Mapped[bool] = mapped_column(Boolean, default=False)
    hosting_model: Mapped[Optional[str]] = mapped_column(String(30))
    operating_region: Mapped[Optional[str]] = mapped_column(String(30))
    integration_method: Mapped[Optional[str]] = mapped_column(String(255))

    # ── Classification ───────────────────────────────
    criticality: Mapped[str] = mapped_column(
        String(20), default=SystemCriticality.MEDIUM.value
    )
    license_model: Mapped[Optional[str]] = mapped_column(String(30))

    # ── Ownership ────────────────────────────────────
    owner_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id")
    )

    # ── Compliance & Access ──────────────────────────
    compliance_notes: Mapped[Optional[str]] = mapped_column(Text)
    url: Mapped[Optional[str]] = mapped_column(String(500))

    # ── Status & Metadata ────────────────────────────
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=CatalogueStatus.EVALUATE.value
    )
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # ── Audit Fields ─────────────────────────────────
    created_by: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id")
    )
    updated_by: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id")
    )

    # ── Relationships ────────────────────────────────
    process_links: Mapped[list["ProcessSystem"]] = relationship(
        back_populates="system",
        cascade="all, delete-orphan",
        lazy="noload",
    )


class ProcessSystem(TenantModel):
    """
    Junction table linking processes to systems with 14 columns.
    Captures how a system is used within a specific process.
    """

    __tablename__ = "process_system"

    # ── Foreign Keys ─────────────────────────────────
    process_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id"), nullable=False, index=True
    )
    system_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("system_catalogue.id"), nullable=False, index=True
    )

    # ── Usage Context ────────────────────────────────
    purpose: Mapped[Optional[str]] = mapped_column(Text)
    system_role: Mapped[str] = mapped_column(
        String(30), default=SystemRole.PRIMARY.value
    )
    integration_method: Mapped[Optional[str]] = mapped_column(String(30))

    # ── Classification ───────────────────────────────
    criticality: Mapped[str] = mapped_column(
        String(20), default=SystemCriticality.MEDIUM.value
    )
    user_scope: Mapped[Optional[str]] = mapped_column(String(255))

    # ── Analysis Fields ──────────────────────────────
    pain_points: Mapped[Optional[str]] = mapped_column(Text)
    automation_potential: Mapped[Optional[str]] = mapped_column(String(20))

    # ── Status ───────────────────────────────────────
    status: Mapped[str] = mapped_column(
        String(20), default=ProcessSystemStatus.ACTIVE.value
    )

    # ── Relationships ────────────────────────────────
    process: Mapped["Process"] = relationship(
        back_populates="system_links",
        foreign_keys=[process_id],
    )
    system: Mapped["SystemCatalogue"] = relationship(
        back_populates="process_links",
        foreign_keys=[system_id],
    )


# Forward reference for type checking
if TYPE_CHECKING:
    from src.models.process import Process
