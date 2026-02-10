"""
Operating Model relational models — dedicated tables for 6 OM components + Role Catalogue.

Blueprint §4.4.1: Replaces JSONB storage for RACI, KPIs, Governance, Policies, Timing, SIPOC
with typed relational tables. Resources, Security, Data remain in JSONB (ProcessOperatingModel).
"""

from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel

import enum


# ── Enums ────────────────────────────────────────────────────


class GovernanceCadence(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    FORTNIGHTLY = "fortnightly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"
    AD_HOC = "ad_hoc"


class PolicyType(str, enum.Enum):
    POLICY = "policy"
    BUSINESS_RULE = "business_rule"
    REGULATORY = "regulatory"
    STANDARD = "standard"
    GUIDELINE = "guideline"


class TimingFrequency(str, enum.Enum):
    CONTINUOUS = "continuous"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"
    PER_ORDER = "per_order"
    ON_DEMAND = "on_demand"


class SipocElement(str, enum.Enum):
    SUPPLIER = "supplier"
    INPUT = "input"
    OUTPUT = "output"
    CUSTOMER = "customer"


class AgenticPotential(str, enum.Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ── Models ───────────────────────────────────────────────────


class RoleCatalogue(TenantModel):
    """Reference table of operational roles for UI dropdowns."""

    __tablename__ = "role_catalogue"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    scope: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class ProcessRaci(TenantModel):
    """RACI matrix entry: one activity row per process."""

    __tablename__ = "process_raci"

    process_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id"), nullable=False, index=True
    )
    activity: Mapped[str] = mapped_column(String(255), nullable=False)
    responsible: Mapped[Optional[str]] = mapped_column(String(255))
    accountable: Mapped[Optional[str]] = mapped_column(String(255))
    consulted: Mapped[Optional[str]] = mapped_column(String(255))
    informed: Mapped[Optional[str]] = mapped_column(String(255))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    process: Mapped["Process"] = relationship(
        back_populates="raci_entries", foreign_keys=[process_id]
    )


class ProcessKpi(TenantModel):
    """KPI/metric attached to a process."""

    __tablename__ = "process_kpi"

    process_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    unit: Mapped[Optional[str]] = mapped_column(String(50))
    target_value: Mapped[Optional[str]] = mapped_column(String(100))
    current_value: Mapped[Optional[str]] = mapped_column(String(100))
    previous_value: Mapped[Optional[str]] = mapped_column(String(100))
    trend: Mapped[Optional[str]] = mapped_column(String(10))
    rag_status: Mapped[Optional[str]] = mapped_column(String(10))
    frequency: Mapped[Optional[str]] = mapped_column(String(50))
    data_source: Mapped[Optional[str]] = mapped_column(String(255))
    owner_role: Mapped[Optional[str]] = mapped_column(String(255))

    process: Mapped["Process"] = relationship(
        back_populates="kpi_entries", foreign_keys=[process_id]
    )


class ProcessGovernance(TenantModel):
    """Governance forum attached to a process."""

    __tablename__ = "process_governance"

    process_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id"), nullable=False, index=True
    )
    forum_name: Mapped[str] = mapped_column(String(255), nullable=False)
    cadence: Mapped[Optional[str]] = mapped_column(String(20))
    chair: Mapped[Optional[str]] = mapped_column(String(255))
    attendees: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    decision_authority: Mapped[Optional[str]] = mapped_column(Text)
    escalation_path: Mapped[Optional[str]] = mapped_column(Text)
    approval_threshold: Mapped[Optional[str]] = mapped_column(Text)
    documentation: Mapped[Optional[str]] = mapped_column(Text)

    process: Mapped["Process"] = relationship(
        back_populates="governance_entries", foreign_keys=[process_id]
    )


class ProcessPolicy(TenantModel):
    """Policy or business rule attached to a process."""

    __tablename__ = "process_policy"

    process_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    policy_type: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    compliance_requirement: Mapped[Optional[str]] = mapped_column(String(255))
    owner_role: Mapped[Optional[str]] = mapped_column(String(255))
    last_reviewed: Mapped[Optional[date]] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    process: Mapped["Process"] = relationship(
        back_populates="policy_entries", foreign_keys=[process_id]
    )


class ProcessTiming(TenantModel):
    """Timing and SLA metric attached to a process."""

    __tablename__ = "process_timing"

    process_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    frequency: Mapped[Optional[str]] = mapped_column(String(20))
    volume_per_period: Mapped[Optional[str]] = mapped_column(String(100))
    cycle_time_target: Mapped[Optional[str]] = mapped_column(String(100))
    cycle_time_actual: Mapped[Optional[str]] = mapped_column(String(100))
    sla_commitment: Mapped[Optional[str]] = mapped_column(Text)
    trigger_event: Mapped[Optional[str]] = mapped_column(Text)
    dependencies: Mapped[Optional[str]] = mapped_column(Text)
    peak_season: Mapped[Optional[str]] = mapped_column(String(255))

    process: Mapped["Process"] = relationship(
        back_populates="timing_entries", foreign_keys=[process_id]
    )


class ProcessSipoc(TenantModel):
    """SIPOC element (Supplier/Input/Output/Customer) attached to a process."""

    __tablename__ = "process_sipoc"

    process_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id"), nullable=False, index=True
    )
    element_type: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    process: Mapped["Process"] = relationship(
        back_populates="sipoc_entries", foreign_keys=[process_id]
    )


# Forward reference for type checking
if TYPE_CHECKING:
    from src.models.process import Process
