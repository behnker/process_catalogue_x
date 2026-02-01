"""
RIADA (Operational Quality Logs) models.

Blueprint §4.3: Risks, Issues, Actions, Dependencies, Assumptions
Blueprint §4.3.2: 4 categories — People, Process, System, Data
Blueprint §4.3.3: Polymorphic attachment to Process, Portfolio, BM
Blueprint §4.3.4: Aggregation rolls up the hierarchy
"""

from datetime import date
from typing import Optional

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel

import enum


class RiadaType(str, enum.Enum):
    RISK = "risk"
    ISSUE = "issue"
    ACTION = "action"
    DEPENDENCY = "dependency"
    ASSUMPTION = "assumption"


class RiadaCategory(str, enum.Enum):
    PEOPLE = "people"
    PROCESS = "process"
    SYSTEM = "system"
    DATA = "data"


class RiadaSeverity(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RiadaStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    MITIGATED = "mitigated"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ACCEPTED = "accepted"


class RiadaItem(TenantModel):
    """
    A single RIADA item (Risk, Issue, Action, Dependency, or Assumption).
    Can be attached to a Process, Portfolio item, or Business Model entry.
    """

    __tablename__ = "riada_items"

    # ── Core Fields ──────────────────────────────────
    code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # ── Classification ───────────────────────────────
    riada_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(
        String(20), default=RiadaSeverity.MEDIUM.value, index=True
    )
    status: Mapped[str] = mapped_column(
        String(20), default=RiadaStatus.OPEN.value, index=True
    )

    # ── Risk-specific fields ─────────────────────────
    probability: Mapped[Optional[int]] = mapped_column(Integer)  # 1-5
    impact: Mapped[Optional[int]] = mapped_column(Integer)  # 1-5
    risk_score: Mapped[Optional[int]] = mapped_column(Integer)  # probability × impact
    mitigation_plan: Mapped[Optional[str]] = mapped_column(Text)

    # ── Action-specific fields ───────────────────────
    due_date: Mapped[Optional[date]] = mapped_column(Date)
    assigned_to_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))
    raised_by_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))

    # ── Polymorphic Attachment (Blueprint §4.3.3) ────
    process_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id"), index=True
    )
    portfolio_item_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("portfolio_items.id"), index=True
    )
    business_model_entry_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("business_model_entries.id"), index=True
    )

    # ── RAG Status ───────────────────────────────────
    rag_status: Mapped[Optional[str]] = mapped_column(String(10))  # red, amber, green

    # ── Resolution ───────────────────────────────────
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text)
    resolved_at: Mapped[Optional[date]] = mapped_column(Date)
    resolved_by_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))

    # ── Metadata ─────────────────────────────────────
    tags: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)

    # ── Relationships ────────────────────────────────
    process: Mapped[Optional["Process"]] = relationship(
        back_populates="riada_items", foreign_keys=[process_id]
    )
    portfolio_item: Mapped[Optional["PortfolioItem"]] = relationship(
        back_populates="riada_items", foreign_keys=[portfolio_item_id]
    )
    business_model_entry: Mapped[Optional["BusinessModelEntry"]] = relationship(
        back_populates="riada_items", foreign_keys=[business_model_entry_id]
    )


# Forward references resolved in __init__
from src.models.process import Process  # noqa: E402, F401
from src.models.portfolio import PortfolioItem  # noqa: E402, F401
from src.models.business_model import BusinessModelEntry  # noqa: E402, F401
