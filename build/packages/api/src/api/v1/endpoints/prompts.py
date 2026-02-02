"""
Prompt Library API endpoints.
Templates, execution, and LLM configuration.

Blueprint §4.4.6: Prompt library with templates and execution tracking.
Blueprint §6.4.11: LLM configuration and usage tracking.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.security import encrypt_sensitive_data
from src.core.tenancy import get_tenant_db
from src.models.reference import LLMConfiguration, PromptExecution, PromptTemplate
from src.schemas.prompts import (
    LLMConfigCreate,
    LLMConfigResponse,
    LLMConfigUpdate,
    PromptExecutionCreate,
    PromptExecutionResponse,
    PromptTemplateCreate,
    PromptTemplateListResponse,
    PromptTemplateResponse,
    PromptTemplateUpdate,
)

router = APIRouter()

VALID_CATEGORIES = {
    "documentation",
    "analysis",
    "improvement",
    "reporting",
    "gap_analysis",
    "process_design",
    "risk_assessment",
}


# ── Prompt Templates ────────────────────────────────────


@router.get("/templates", response_model=PromptTemplateListResponse)
async def list_templates(
    category: Optional[str] = Query(None),
    context_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List prompt templates."""
    query = select(PromptTemplate).where(
        PromptTemplate.organization_id == user.organization_id,
        PromptTemplate.is_published == True,
    )

    if category:
        query = query.where(PromptTemplate.category == category)
    if context_type:
        query = query.where(PromptTemplate.context_type == context_type)
    if search:
        query = query.where(
            PromptTemplate.name.ilike(f"%{search}%")
            | PromptTemplate.description.ilike(f"%{search}%")
        )

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(PromptTemplate.usage_count.desc(), PromptTemplate.name)
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    templates = result.scalars().all()

    return PromptTemplateListResponse(
        items=[PromptTemplateResponse.model_validate(t) for t in templates],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/templates/{template_id}", response_model=PromptTemplateResponse)
async def get_template(
    template_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get a prompt template."""
    result = await db.execute(
        select(PromptTemplate).where(
            PromptTemplate.id == template_id,
            PromptTemplate.organization_id == user.organization_id,
        )
    )
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    return PromptTemplateResponse.model_validate(template)


@router.post(
    "/templates",
    response_model=PromptTemplateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_template(
    body: PromptTemplateCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new prompt template."""
    if body.category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Must be one of: {', '.join(VALID_CATEGORIES)}",
        )

    template = PromptTemplate(
        id=str(uuid4()),
        organization_id=user.organization_id,
        is_system=False,
        **body.model_dump(),
    )
    db.add(template)
    await db.flush()
    await db.refresh(template)

    return PromptTemplateResponse.model_validate(template)


@router.patch("/templates/{template_id}", response_model=PromptTemplateResponse)
async def update_template(
    template_id: str,
    body: PromptTemplateUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a prompt template."""
    result = await db.execute(
        select(PromptTemplate).where(
            PromptTemplate.id == template_id,
            PromptTemplate.organization_id == user.organization_id,
            PromptTemplate.is_system == False,  # Can't edit system templates
        )
    )
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found or not editable")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template, field, value)

    await db.flush()
    await db.refresh(template)

    return PromptTemplateResponse.model_validate(template)


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a prompt template (unpublish)."""
    result = await db.execute(
        select(PromptTemplate).where(
            PromptTemplate.id == template_id,
            PromptTemplate.organization_id == user.organization_id,
            PromptTemplate.is_system == False,
        )
    )
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found or not deletable")

    template.is_published = False
    await db.flush()


# ── Prompt Execution ────────────────────────────────────


@router.post("/execute", response_model=PromptExecutionResponse)
async def execute_prompt(
    body: PromptExecutionCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Execute a prompt against a target entity.
    This records the execution - actual LLM call is handled by the service layer.
    """
    # Get LLM config
    result = await db.execute(
        select(LLMConfiguration).where(
            LLMConfiguration.organization_id == user.organization_id,
            LLMConfiguration.is_enabled == True,
        )
    )
    llm_config = result.scalar_one_or_none()

    if not llm_config:
        raise HTTPException(
            status_code=400,
            detail="No LLM configuration found. Please configure an LLM provider.",
        )

    # Update template usage count if using a template
    if body.template_id:
        result = await db.execute(
            select(PromptTemplate).where(PromptTemplate.id == body.template_id)
        )
        template = result.scalar_one_or_none()
        if template:
            template.usage_count += 1

    # Create execution record
    execution = PromptExecution(
        id=str(uuid4()),
        organization_id=user.organization_id,
        template_id=body.template_id,
        user_id=user.id,
        target_entity_type=body.target_entity_type,
        target_entity_id=body.target_entity_id,
        prompt_sent=body.prompt_text,
        model_used=llm_config.model,
        # Response fields will be updated by the LLM service
    )
    db.add(execution)
    await db.flush()
    await db.refresh(execution)

    return PromptExecutionResponse.model_validate(execution)


@router.get("/executions", response_model=list[PromptExecutionResponse])
async def list_executions(
    template_id: Optional[str] = Query(None),
    target_entity_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List recent prompt executions."""
    query = select(PromptExecution).where(
        PromptExecution.organization_id == user.organization_id,
        PromptExecution.user_id == user.id,
    )

    if template_id:
        query = query.where(PromptExecution.template_id == template_id)
    if target_entity_type:
        query = query.where(PromptExecution.target_entity_type == target_entity_type)

    query = query.order_by(PromptExecution.created_at.desc()).limit(limit)

    result = await db.execute(query)
    executions = result.scalars().all()

    return [PromptExecutionResponse.model_validate(e) for e in executions]


# ── LLM Configuration ───────────────────────────────────


@router.get("/llm-config", response_model=list[LLMConfigResponse])
async def list_llm_configs(
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List LLM configurations for the organization."""
    result = await db.execute(
        select(LLMConfiguration).where(
            LLMConfiguration.organization_id == user.organization_id
        )
    )
    configs = result.scalars().all()
    return [LLMConfigResponse.model_validate(c) for c in configs]


@router.post(
    "/llm-config",
    response_model=LLMConfigResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_llm_config(
    body: LLMConfigCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create an LLM configuration."""
    # Encrypt API key before storage
    config_data = body.model_dump()
    if config_data.get("api_key_encrypted"):
        config_data["api_key_encrypted"] = encrypt_sensitive_data(
            config_data["api_key_encrypted"]
        )

    config = LLMConfiguration(
        id=str(uuid4()),
        organization_id=user.organization_id,
        **config_data,
    )
    db.add(config)
    await db.flush()
    await db.refresh(config)

    return LLMConfigResponse.model_validate(config)


@router.patch("/llm-config/{config_id}", response_model=LLMConfigResponse)
async def update_llm_config(
    config_id: str,
    body: LLMConfigUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update an LLM configuration."""
    result = await db.execute(
        select(LLMConfiguration).where(
            LLMConfiguration.id == config_id,
            LLMConfiguration.organization_id == user.organization_id,
        )
    )
    config = result.scalar_one_or_none()

    if not config:
        raise HTTPException(status_code=404, detail="LLM configuration not found")

    update_data = body.model_dump(exclude_unset=True)
    # Encrypt API key if being updated
    if "api_key_encrypted" in update_data and update_data["api_key_encrypted"]:
        update_data["api_key_encrypted"] = encrypt_sensitive_data(
            update_data["api_key_encrypted"]
        )

    for field, value in update_data.items():
        setattr(config, field, value)

    await db.flush()
    await db.refresh(config)

    return LLMConfigResponse.model_validate(config)


@router.delete("/llm-config/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_llm_config(
    config_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete an LLM configuration."""
    result = await db.execute(
        select(LLMConfiguration).where(
            LLMConfiguration.id == config_id,
            LLMConfiguration.organization_id == user.organization_id,
        )
    )
    config = result.scalar_one_or_none()

    if not config:
        raise HTTPException(status_code=404, detail="LLM configuration not found")

    await db.delete(config)
    await db.flush()
