"""
Reference Data Catalogues and Prompt Library models.

Blueprint §5.1: Lifecycle status values
Blueprint §5.2: 9 reference catalogues
Blueprint §4.4.6: Prompt library with templates, execution tracking
Blueprint §6.4.11: LLM configuration and usage tracking
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel


# ── Reference Data Catalogues (Blueprint §5.2) ──────

class ReferenceCatalogue(TenantModel):
    """
    Configurable reference data.
    9 catalogues: roles, systems, clients, markets, categories,
    partners, suppliers, functions, departments.
    """

    __tablename__ = "reference_catalogues"

    catalogue_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="active")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    parent_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))
    metadata_extra: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)


# ── Prompt Library (Blueprint §4.4.6) ────────────────

class PromptTemplate(TenantModel):
    """
    Reusable AI prompt template.
    Can be run against any process, project, or RIADA item.
    """

    __tablename__ = "prompt_templates"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    # categories: documentation, analysis, improvement, reporting, gap_analysis

    # Template content with {{variable}} placeholders
    system_prompt: Mapped[Optional[str]] = mapped_column(Text)
    user_prompt_template: Mapped[str] = mapped_column(Text, nullable=False)

    # Context configuration
    context_type: Mapped[str] = mapped_column(String(30), default="process")
    include_riada: Mapped[bool] = mapped_column(Boolean, default=True)
    include_kpis: Mapped[bool] = mapped_column(Boolean, default=False)
    include_raci: Mapped[bool] = mapped_column(Boolean, default=False)

    # Execution defaults
    default_model: Mapped[Optional[str]] = mapped_column(String(100))
    default_temperature: Mapped[Optional[float]] = mapped_column(Numeric(3, 2))
    default_max_tokens: Mapped[Optional[int]] = mapped_column(Integer)

    # Metadata
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)  # built-in vs user-created
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_rating: Mapped[Optional[float]] = mapped_column(Numeric(3, 2))
    tags: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)


class PromptExecution(TenantModel):
    """
    Record of a prompt being executed against a target entity.
    Tracks input, output, tokens, cost, and user feedback.
    """

    __tablename__ = "prompt_executions"

    template_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("prompt_templates.id"), index=True
    )
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)

    # Target entity (polymorphic)
    target_entity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    target_entity_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)

    # Input / Output
    prompt_sent: Mapped[str] = mapped_column(Text, nullable=False)
    response_received: Mapped[Optional[str]] = mapped_column(Text)
    model_used: Mapped[str] = mapped_column(String(100), nullable=False)

    # Token tracking
    prompt_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    completion_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    total_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    estimated_cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 6))

    # Feedback
    rating: Mapped[Optional[int]] = mapped_column(Integer)  # 1-5
    feedback: Mapped[Optional[str]] = mapped_column(Text)
    is_saved: Mapped[bool] = mapped_column(Boolean, default=False)

    # Execution metadata
    execution_time_ms: Mapped[Optional[int]] = mapped_column(Integer)
    error_message: Mapped[Optional[str]] = mapped_column(Text)


# ── LLM Configuration (Blueprint §6.4.11) ────────────

class LLMConfiguration(TenantModel):
    """Per-tenant LLM provider configuration."""

    __tablename__ = "llm_configurations"

    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    api_key_encrypted: Mapped[Optional[str]] = mapped_column(Text)
    endpoint_url: Mapped[Optional[str]] = mapped_column(String(500))
    default_temperature: Mapped[float] = mapped_column(Numeric(3, 2), default=0.7)
    default_max_tokens: Mapped[int] = mapped_column(Integer, default=4000)
    rate_limit_rpm: Mapped[int] = mapped_column(Integer, default=60)
    monthly_token_limit: Mapped[Optional[int]] = mapped_column(Integer)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
