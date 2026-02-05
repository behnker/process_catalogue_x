"""
Issue & Opportunity Log models.

Operational issues tied to processes with auto-sync to process RAG status.
OPS- prefix distinguishes from RIADA project issues (ISS-).

Sources:
- Additional Design Documents/ISSUE_OPPORTUNITY_LOG_SPEC.docx
- Additional Design Documents/RAG_Issue_Alignment_Addendum.docx
- Additional Design Documents/Implementation_Amendments.docx (AMD-01: OPS- prefix)
"""

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel, BaseModel

import enum


class IssueClassification(str, enum.Enum):
    """Classification of operational issues (matches 4 RAG dimensions)."""
    PEOPLE = "people"
    PROCESS = "process"
    SYSTEM = "system"
    DATA = "data"


class IssueCriticality(str, enum.Enum):
    """Criticality levels that drive RAG status."""
    HIGH = "high"      # -> RED in process RAG
    MEDIUM = "medium"  # -> AMBER in process RAG
    LOW = "low"        # -> AMBER in process RAG


class IssueComplexity(str, enum.Enum):
    """Complexity of resolution (for effort estimation)."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IssueStatus(str, enum.Enum):
    """Issue lifecycle states."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    DEFERRED = "deferred"


class OpportunityStatus(str, enum.Enum):
    """Status of improvement opportunities identified from issues."""
    IDENTIFIED = "identified"
    EVALUATING = "evaluating"
    APPROVED = "approved"
    IN_DELIVERY = "in_delivery"
    DELIVERED = "delivered"
    REJECTED = "rejected"


class RagStatus(str, enum.Enum):
    """RAG status values for process dimensions."""
    RED = "red"
    AMBER = "amber"
    GREEN = "green"
    NEUTRAL = "neutral"


class IssueLog(TenantModel):
    """
    Operational issue tied to a process.

    Auto-numbered as OPS-001, OPS-002, etc. per organization.
    Issue criticality drives process RAG status via DB trigger.
    """

    __tablename__ = "issue_log"

    # Auto-incremented per org (trigger-managed)
    issue_number: Mapped[int] = mapped_column(Integer, nullable=False)

    # Core fields
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # Classification (separate from RIADA - allows independent evolution)
    # Use PostgreSQL ENUM types (created in migration 009)
    issue_classification: Mapped[str] = mapped_column(
        ENUM('people', 'process', 'system', 'data',
             name='issue_classification', create_type=False),
        nullable=False
    )
    issue_criticality: Mapped[str] = mapped_column(
        ENUM('high', 'medium', 'low',
             name='issue_criticality', create_type=False),
        nullable=False, default=IssueCriticality.MEDIUM.value
    )
    issue_complexity: Mapped[str] = mapped_column(
        ENUM('high', 'medium', 'low',
             name='issue_complexity', create_type=False),
        nullable=False, default=IssueComplexity.MEDIUM.value
    )

    # Status workflow
    issue_status: Mapped[str] = mapped_column(
        ENUM('open', 'in_progress', 'resolved', 'closed', 'deferred',
             name='issue_status', create_type=False),
        nullable=False, default=IssueStatus.OPEN.value, index=True
    )

    # Process linkage (denormalized for heatmap performance)
    process_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id"), nullable=False, index=True
    )
    process_level: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 0-5
    process_ref: Mapped[str] = mapped_column(String(20), nullable=False)  # Frozen code
    process_name: Mapped[str] = mapped_column(String(255), nullable=False)  # Frozen name

    # Ownership
    raised_by_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    assigned_to_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id")
    )

    # Dates
    date_raised: Mapped[date] = mapped_column(Date, nullable=False)
    target_resolution_date: Mapped[Optional[date]] = mapped_column(Date)
    actual_resolution_date: Mapped[Optional[date]] = mapped_column(Date)

    # Resolution
    resolution_summary: Mapped[Optional[str]] = mapped_column(Text)

    # Opportunity tracking
    opportunity_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    opportunity_status: Mapped[Optional[str]] = mapped_column(
        ENUM('identified', 'evaluating', 'approved', 'in_delivery', 'delivered', 'rejected',
             name='opportunity_status', create_type=False)
    )
    opportunity_description: Mapped[Optional[str]] = mapped_column(Text)
    opportunity_expected_benefit: Mapped[Optional[str]] = mapped_column(Text)
    opportunity_beneficiary_roles: Mapped[Optional[list]] = mapped_column(
        JSONB, nullable=True
    )  # AMD-02: JSONB not TEXT[]

    # Audit trail
    created_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    updated_by: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id")
    )

    # Relationships
    process: Mapped["Process"] = relationship(
        back_populates="issues", foreign_keys=[process_id]
    )

    @property
    def display_id(self) -> str:
        """AMD-01: OPS- prefix for display."""
        return f"OPS-{self.issue_number:03d}"


class IssueLogHistory(BaseModel):
    """
    Field-level change history for issues.

    User-facing timeline with change notes (distinct from AuditLog compliance trail).
    """

    __tablename__ = "issue_log_history"

    organization_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("organizations.id"), nullable=False, index=True
    )
    issue_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("issue_log.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    # What changed
    field_name: Mapped[str] = mapped_column(String(50), nullable=False)
    old_value: Mapped[Optional[str]] = mapped_column(Text)
    new_value: Mapped[Optional[str]] = mapped_column(Text)

    # User note
    change_note: Mapped[Optional[str]] = mapped_column(Text)

    # Who and when
    changed_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    changed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# Forward reference resolution
from src.models.process import Process  # noqa: E402, F401
