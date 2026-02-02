"""RIADA item linking endpoints.

Blueprint §5.3.6: Risk → Linked Actions, Issue → Linked Dependencies, etc.
"""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.riada import RiadaItem, RiadaLink
from src.schemas.riada import (
    RIADA_LINK_TYPES,
    RiadaLinkCreate,
    RiadaLinkResponse,
    RiadaLinkedItemBrief,
    RiadaLinksResponse,
)

router = APIRouter()


@router.get("/{riada_id}/links", response_model=RiadaLinksResponse)
async def get_riada_links(
    riada_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get all links for a RIADA item (both outgoing and incoming)."""
    # Verify item exists
    result = await db.execute(
        select(RiadaItem)
        .where(
            RiadaItem.id == riada_id,
            RiadaItem.organization_id == user.organization_id,
        )
        .options(
            selectinload(RiadaItem.outgoing_links).selectinload(RiadaLink.target),
            selectinload(RiadaItem.incoming_links).selectinload(RiadaLink.source),
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="RIADA item not found")

    # Build outgoing links (this item is the source)
    outgoing = [
        RiadaLinkedItemBrief(
            id=link.target.id,
            code=link.target.code,
            title=link.target.title,
            riada_type=link.target.riada_type,
            severity=link.target.severity,
            status=link.target.status,
            link_id=link.id,
            link_type=link.link_type,
            link_direction="outgoing",
        )
        for link in item.outgoing_links
        if link.target  # Ensure target exists
    ]

    # Build incoming links (this item is the target)
    incoming = [
        RiadaLinkedItemBrief(
            id=link.source.id,
            code=link.source.code,
            title=link.source.title,
            riada_type=link.source.riada_type,
            severity=link.source.severity,
            status=link.source.status,
            link_id=link.id,
            link_type=link.link_type,
            link_direction="incoming",
        )
        for link in item.incoming_links
        if link.source  # Ensure source exists
    ]

    return RiadaLinksResponse(
        riada_id=riada_id,
        outgoing=outgoing,
        incoming=incoming,
        total=len(outgoing) + len(incoming),
    )


@router.post(
    "/{riada_id}/links",
    response_model=RiadaLinkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_riada_link(
    riada_id: str,
    body: RiadaLinkCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a link from this RIADA item to another."""
    # Validate link type
    if body.link_type not in RIADA_LINK_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid link type. Must be one of: {', '.join(RIADA_LINK_TYPES)}",
        )

    # Cannot link to self
    if riada_id == body.target_id:
        raise HTTPException(status_code=400, detail="Cannot link an item to itself")

    # Verify source item exists
    result = await db.execute(
        select(RiadaItem).where(
            RiadaItem.id == riada_id,
            RiadaItem.organization_id == user.organization_id,
        )
    )
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source RIADA item not found")

    # Verify target item exists and belongs to same org
    result = await db.execute(
        select(RiadaItem).where(
            RiadaItem.id == body.target_id,
            RiadaItem.organization_id == user.organization_id,
        )
    )
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail="Target RIADA item not found")

    # Check for existing link (prevent duplicates)
    result = await db.execute(
        select(RiadaLink).where(
            RiadaLink.source_id == riada_id,
            RiadaLink.target_id == body.target_id,
            RiadaLink.organization_id == user.organization_id,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409, detail="A link between these items already exists"
        )

    # Create link
    link = RiadaLink(
        id=str(uuid4()),
        organization_id=user.organization_id,
        source_id=riada_id,
        target_id=body.target_id,
        link_type=body.link_type,
        notes=body.notes,
    )
    db.add(link)
    await db.flush()
    await db.refresh(link)

    return RiadaLinkResponse.model_validate(link)


@router.delete("/{riada_id}/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_riada_link(
    riada_id: str,
    link_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a link from a RIADA item."""
    # Find link (must involve this riada_id as source or target)
    result = await db.execute(
        select(RiadaLink).where(
            RiadaLink.id == link_id,
            RiadaLink.organization_id == user.organization_id,
            or_(
                RiadaLink.source_id == riada_id,
                RiadaLink.target_id == riada_id,
            ),
        )
    )
    link = result.scalar_one_or_none()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    await db.delete(link)
    await db.flush()


@router.patch("/{riada_id}/links/{link_id}", response_model=RiadaLinkResponse)
async def update_riada_link(
    riada_id: str,
    link_id: str,
    body: RiadaLinkCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a link's type or notes."""
    # Validate link type
    if body.link_type not in RIADA_LINK_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid link type. Must be one of: {', '.join(RIADA_LINK_TYPES)}",
        )

    # Find link
    result = await db.execute(
        select(RiadaLink).where(
            RiadaLink.id == link_id,
            RiadaLink.organization_id == user.organization_id,
            RiadaLink.source_id == riada_id,
        )
    )
    link = result.scalar_one_or_none()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    # Update fields
    link.link_type = body.link_type
    if body.notes is not None:
        link.notes = body.notes

    await db.flush()
    await db.refresh(link)

    return RiadaLinkResponse.model_validate(link)
