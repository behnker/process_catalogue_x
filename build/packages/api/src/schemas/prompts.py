"""
Prompt Library API schemas.

Blueprint §4.4.6: Prompt templates and execution.
Blueprint §6.4.11: LLM configuration.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Prompt Templates ────────────────────────────────────


class PromptTemplateCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    category: str  # documentation, analysis, improvement, reporting, gap_analysis, process_design, risk_assessment
    system_prompt: Optional[str] = None
    user_prompt_template: str
    context_type: str = "process"  # process, riada, portfolio, business_model
    include_riada: bool = True
    include_kpis: bool = False
    include_raci: bool = False
    default_model: Optional[str] = None
    default_temperature: Optional[float] = Field(None, ge=0, le=2)
    default_max_tokens: Optional[int] = Field(None, ge=1, le=100000)
    is_published: bool = True
    tags: list[str] = []


class PromptTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    system_prompt: Optional[str] = None
    user_prompt_template: Optional[str] = None
    context_type: Optional[str] = None
    include_riada: Optional[bool] = None
    include_kpis: Optional[bool] = None
    include_raci: Optional[bool] = None
    default_model: Optional[str] = None
    default_temperature: Optional[float] = None
    default_max_tokens: Optional[int] = None
    is_published: Optional[bool] = None
    tags: Optional[list[str]] = None


class PromptTemplateResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    category: str
    system_prompt: Optional[str]
    user_prompt_template: str
    context_type: str
    include_riada: bool
    include_kpis: bool
    include_raci: bool
    default_model: Optional[str]
    default_temperature: Optional[float]
    default_max_tokens: Optional[int]
    is_system: bool
    is_published: bool
    usage_count: int
    avg_rating: Optional[float]
    tags: list
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PromptTemplateListResponse(BaseModel):
    items: list[PromptTemplateResponse]
    total: int
    page: int = 1
    page_size: int = 50


# ── Prompt Execution ────────────────────────────────────


class PromptExecutionCreate(BaseModel):
    template_id: Optional[str] = None
    target_entity_type: str  # process, riada, portfolio, business_model
    target_entity_id: str
    prompt_text: str  # The actual prompt to send


class PromptExecutionResponse(BaseModel):
    id: str
    template_id: Optional[str]
    user_id: str
    target_entity_type: str
    target_entity_id: str
    prompt_sent: str
    response_received: Optional[str]
    model_used: str
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]
    estimated_cost: Optional[float]
    rating: Optional[int]
    feedback: Optional[str]
    is_saved: bool
    execution_time_ms: Optional[int]
    error_message: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── LLM Configuration ───────────────────────────────────


class LLMConfigCreate(BaseModel):
    provider: str  # anthropic, openai, alibaba_qwen, baidu_ernie
    model: str
    api_key_encrypted: Optional[str] = None  # Will be encrypted before storage
    endpoint_url: Optional[str] = None
    default_temperature: float = 0.7
    default_max_tokens: int = 4000
    rate_limit_rpm: int = 60
    monthly_token_limit: Optional[int] = None
    is_enabled: bool = True


class LLMConfigUpdate(BaseModel):
    model: Optional[str] = None
    api_key_encrypted: Optional[str] = None
    endpoint_url: Optional[str] = None
    default_temperature: Optional[float] = None
    default_max_tokens: Optional[int] = None
    rate_limit_rpm: Optional[int] = None
    monthly_token_limit: Optional[int] = None
    is_enabled: Optional[bool] = None


class LLMConfigResponse(BaseModel):
    id: str
    provider: str
    model: str
    endpoint_url: Optional[str]
    default_temperature: float
    default_max_tokens: int
    rate_limit_rpm: int
    monthly_token_limit: Optional[int]
    is_enabled: bool
    created_at: datetime
    updated_at: datetime

    # Note: api_key_encrypted is never returned for security

    model_config = {"from_attributes": True}
