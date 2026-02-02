"""Prompt execution endpoints."""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.reference import LLMConfiguration, PromptExecution, PromptTemplate
from src.schemas.prompts import (
    PromptExecutionCreate,
    PromptExecutionResponse,
)

router = APIRouter()


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
