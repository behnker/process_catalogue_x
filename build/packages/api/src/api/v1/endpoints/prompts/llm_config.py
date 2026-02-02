"""LLM configuration endpoints."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.security import encrypt_sensitive_data
from src.core.tenancy import get_tenant_db
from src.models.reference import LLMConfiguration
from src.schemas.prompts import (
    LLMConfigCreate,
    LLMConfigResponse,
    LLMConfigUpdate,
)

router = APIRouter()


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
