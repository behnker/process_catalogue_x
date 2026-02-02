"""Portfolio tree endpoint."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.portfolio import PortfolioItem
from src.schemas.portfolio import PortfolioTreeNode
from src.services.tree_builder import build_tree

router = APIRouter()


@router.get("/tree", response_model=list[PortfolioTreeNode])
async def get_portfolio_tree(
    root_level: str = Query("strategy", description="Starting level for tree"),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get portfolio hierarchy as a tree structure."""
    result = await db.execute(
        select(PortfolioItem)
        .where(PortfolioItem.organization_id == user.organization_id)
        .order_by(PortfolioItem.level, PortfolioItem.sort_order)
    )
    all_items = result.scalars().all()

    def node_factory(item: PortfolioItem, children: list[PortfolioTreeNode]) -> PortfolioTreeNode:
        return PortfolioTreeNode(
            id=item.id,
            code=item.code,
            name=item.name,
            level=item.level,
            status=item.status,
            rag_status=item.rag_status,
            wsvf_score=float(item.wsvf_score) if item.wsvf_score else None,
            sort_order=item.sort_order,
            children=children,
        )

    return build_tree(all_items, node_factory, root_parent_id=None)
