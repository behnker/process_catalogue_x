"""
Business Model models.

Blueprint §4.1: Business Model Canvas with 9 components.
Blueprint §4.1.3: RIADA attachment at business model level.
Blueprint §4.1.4: Agentic opportunity fields.
"""

from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel


class BusinessModel(TenantModel):
    """
    Top-level Business Model entity per organization.
    Contains the 9 BMC components via BusinessModelEntry children.
    """

    __tablename__ = "business_models"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="active")

    # Canvas metadata
    canvas_layout: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)

    # Relationships
    entries: Mapped[list["BusinessModelEntry"]] = relationship(
        back_populates="business_model", lazy="selectin"
    )


class BusinessModelEntry(TenantModel):
    """
    Individual entry within a BMC component.
    E.g., a Key Partner, a Revenue Stream, a Customer Segment.
    """

    __tablename__ = "business_model_entries"

    business_model_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("business_models.id"), nullable=False, index=True
    )

    # BMC Component (9 boxes)
    component: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    # key_partners, key_activities, key_resources, value_propositions,
    # customer_relationships, channels, customer_segments,
    # cost_structure, revenue_streams

    # Entry content
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # Agentic opportunity fields (Blueprint §4.1.4)
    agentic_opportunity: Mapped[Optional[str]] = mapped_column(Text)
    agentic_readiness: Mapped[Optional[str]] = mapped_column(String(20))  # low, medium, high
    agentic_impact: Mapped[Optional[str]] = mapped_column(String(20))
    agentic_notes: Mapped[Optional[str]] = mapped_column(Text)

    # Metadata
    metadata_extra: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)

    # Relationships
    business_model: Mapped["BusinessModel"] = relationship(back_populates="entries")
    riada_items: Mapped[list["RiadaItem"]] = relationship(
        back_populates="business_model_entry",
        foreign_keys="RiadaItem.business_model_entry_id",
        lazy="noload",
    )


class BusinessModelMapping(TenantModel):
    """
    Links processes to business model dimensions.
    Maps from the Business_Model_Integration_Guide.md
    """

    __tablename__ = "business_model_mappings"

    process_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("processes.id"), nullable=False, index=True
    )

    # Business model dimensions
    trading_markets: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)
    clients: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)
    sourcing_markets: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)
    product_categories: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)
    key_partners: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)
    key_suppliers: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)
    channel: Mapped[Optional[str]] = mapped_column(String(50))
    revenue_line: Mapped[Optional[str]] = mapped_column(String(100))
    cost_line: Mapped[Optional[str]] = mapped_column(String(100))
    functions: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)
    value_proposition: Mapped[Optional[str]] = mapped_column(Text)
    customer_segment: Mapped[Optional[str]] = mapped_column(String(255))
    notes: Mapped[Optional[str]] = mapped_column(Text)


# Forward ref
from src.models.riada import RiadaItem  # noqa: E402, F401
