"""Prompt template CRUD endpoints."""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.reference import PromptTemplate
from src.schemas.prompts import (
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
