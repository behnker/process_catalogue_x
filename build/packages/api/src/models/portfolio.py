"""
Portfolio Response models.

Blueprint §4.5: 7-level hierarchy (Strategy → Epic → Task)
Blueprint §4.5.2: WSVF prioritization methodology
Blueprint §4.5.3: Portfolio entities with light PM features
Blueprint §4.5.4: Milestones, budget tracking, team allocation
"""

from datetime import date
from typing import Optional

from sqlalchemy import Boolean, Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel

import enum


class PortfolioLevel(str, enum.Enum):
    STRATEGY = "strategy"        # L0 - Strategic theme
    PORTFOLIO = "portfolio"      # L1 - Portfolio grouping
    PROGRAMME = "programme"      # L2 - Programme
    PROJECT = "project"          # L3 - Project
    WORKSTREAM = "workstream"    # L4 - Workstream
    EPIC = "epic"               # L5 - Epic / deliverable
    TASK = "task"               # L6 - Task


class PortfolioStatus(str, enum.Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PortfolioItem(TenantModel):
    """
    A single item in the portfolio hierarchy (project, programme, etc.).
    Supports 7 levels of hierarchy with RIADA attachment at each.
    """

    __tablename__ = "portfolio_items"

    # ── Identity ────────────────────────────────────
    code: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # ── Hierarchy ───────────────────────────────────
    level: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    parent_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("portfolio_items.id")
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # ── Status & RAG ────────────────────────────────
    status: Mapped[str] = mapped_column(
        String(20), default=PortfolioStatus.PROPOSED.value, index=True
    )
    rag_status: Mapped[Optional[str]] = mapped_column(String(10))  # red, amber, green
    rag_notes: Mapped[Optional[str]] = mapped_column(Text)

    # ── WSVF Prioritization (Blueprint §4.5.2) ──────
    business_value: Mapped[Optional[int]] = mapped_column(Integer)  # 1-10
    time_criticality: Mapped[Optional[int]] = mapped_column(Integer)  # 1-10
    risk_reduction: Mapped[Optional[int]] = mapped_column(Integer)  # 1-10
    job_size: Mapped[Optional[int]] = mapped_column(Integer)  # 1-10 (denominator)
    wsvf_score: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))

    # ── Dates ───────────────────────────────────────
    planned_start: Mapped[Optional[date]] = mapped_column(Date)
    planned_end: Mapped[Optional[date]] = mapped_column(Date)
    actual_start: Mapped[Optional[date]] = mapped_column(Date)
    actual_end: Mapped[Optional[date]] = mapped_column(Date)

    # ── Budget (Blueprint §4.5.4) ────────────────────
    budget_approved: Mapped[Optional[float]] = mapped_column(Numeric(14, 2))
    budget_spent: Mapped[Optional[float]] = mapped_column(Numeric(14, 2))
    budget_forecast: Mapped[Optional[float]] = mapped_column(Numeric(14, 2))
    budget_currency: Mapped[str] = mapped_column(String(3), default="USD")

    # ── Ownership ───────────────────────────────────
    owner_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))
    sponsor_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))

    # ── Process Linkage (Blueprint §4.5.11) ──────────
    linked_process_ids: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    # ── Metadata ────────────────────────────────────
    tags: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    metadata_extra: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # ── Relationships ───────────────────────────────
    parent: Mapped[Optional["PortfolioItem"]] = relationship(
        back_populates="children", remote_side="PortfolioItem.id"
    )
    children: Mapped[list["PortfolioItem"]] = relationship(
        back_populates="parent", lazy="selectin"
    )
    milestones: Mapped[list["PortfolioMilestone"]] = relationship(
        back_populates="portfolio_item", lazy="selectin"
    )
    riada_items: Mapped[list["RiadaItem"]] = relationship(
        back_populates="portfolio_item",
        foreign_keys="RiadaItem.portfolio_item_id",
        lazy="noload",
    )


class PortfolioMilestone(TenantModel):
    """
    Milestones within a portfolio item.
    Blueprint §4.5.4: Light PM — milestone tracking.
    """

    __tablename__ = "portfolio_milestones"

    portfolio_item_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("portfolio_items.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    due_date: Mapped[Optional[date]] = mapped_column(Date)
    completed_date: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    portfolio_item: Mapped["PortfolioItem"] = relationship(back_populates="milestones")


# Forward ref
from src.models.riada import RiadaItem  # noqa: E402, F401
