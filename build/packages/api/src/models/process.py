"""
Process Catalogue models — the Process Spine.

Blueprint §3.1: The Process Spine is the backbone of the entire platform.
Blueprint §4.2: 6-level hierarchy (L0–L5) with primary/secondary classification.
Blueprint §4.2.1: Primary processes (SOURCE, DEVELOP, EXECUTE) vs
                   Secondary processes (DATA, PEOPLE, FINANCE, COMPLIANCE).
"""

from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel

import enum


class ProcessType(str, enum.Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


class ProcessLevel(str, enum.Enum):
    L0 = "L0"  # Value Stream (e.g., SOURCE, DEVELOP, EXECUTE, SUPPORT)
    L1 = "L1"  # Process Group (e.g., Client Intake & Commercial Setup)
    L2 = "L2"  # Process (e.g., Brief, Quote, Vendor Engagement)
    L3 = "L3"  # Workflow / Sub-Process
    L4 = "L4"  # Variation (by market, category, client)
    L5 = "L5"  # Step / Task


class LifecycleStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class AutomationLevel(str, enum.Enum):
    MANUAL = "manual"
    SEMI_AUTOMATED = "semi_automated"
    FULLY_AUTOMATED = "fully_automated"
    AI_ASSISTED = "ai_assisted"


class Process(TenantModel):
    """
    Central entity: a process at any level in the 6-level hierarchy.
    This is the Process Spine — every other component attaches here.
    """

    __tablename__ = "processes"

    # ── Identity ────────────────────────────────────
    code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # e.g., L2-10
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # ── Hierarchy ───────────────────────────────────
    level: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    parent_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id")
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # ── Classification ──────────────────────────────
    process_type: Mapped[str] = mapped_column(
        String(20), default=ProcessType.PRIMARY.value
    )
    status: Mapped[str] = mapped_column(
        String(20), default=LifecycleStatus.DRAFT.value, index=True
    )

    # ── Automation Tracking (Blueprint §4.2) ────────
    current_automation: Mapped[str] = mapped_column(
        String(30), default=AutomationLevel.MANUAL.value
    )
    target_automation: Mapped[Optional[str]] = mapped_column(String(30))
    automation_notes: Mapped[Optional[str]] = mapped_column(Text)

    # ── Ownership ───────────────────────────────────
    owner_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))
    sponsor_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))
    function_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))

    # ── Metadata ────────────────────────────────────
    tags: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    metadata_extra: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # ── Relationships ───────────────────────────────
    parent: Mapped[Optional["Process"]] = relationship(
        back_populates="children", remote_side="Process.id"
    )
    children: Mapped[list["Process"]] = relationship(
        back_populates="parent", lazy="selectin"
    )
    operating_model: Mapped[list["ProcessOperatingModel"]] = relationship(
        back_populates="process", lazy="selectin"
    )
    riada_items: Mapped[list["RiadaItem"]] = relationship(
        back_populates="process", lazy="noload",
        foreign_keys="RiadaItem.process_id"
    )


# ── Operating Model Components (Blueprint §4.4.1) ───

class ProcessOperatingModel(TenantModel):
    """
    Operating model components attached to a process.
    Blueprint §4.4.1: 10 components (RACI, KPIs, Policies, Systems, etc.)
    Each component stores Current State and Future State.
    """

    __tablename__ = "process_operating_model"

    process_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id"), nullable=False, index=True
    )
    component_type: Mapped[str] = mapped_column(
        String(30), nullable=False, index=True
    )  # raci, kpis, policies, systems, timing, governance, sipoc, resources, risks, controls

    # Current / Future state (Blueprint §4.4.4)
    current_state: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    future_state: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    transition_notes: Mapped[Optional[str]] = mapped_column(Text)

    process: Mapped["Process"] = relationship(back_populates="operating_model")


# Import here to avoid circular — these are in separate model files
# but we declare the string-based relationship above
from src.models.riada import RiadaItem  # noqa: E402, F401
