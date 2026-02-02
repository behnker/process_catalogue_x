"""
Portfolio API endpoints - split into sub-routers.

Full CRUD with hierarchy, WSVF scoring, and milestones.

Blueprint §4.5: 7-level hierarchy (Strategy → Epic → Task)
Blueprint §4.5.2: WSVF prioritization
Blueprint §4.5.4: Milestones, budget tracking
"""

from fastapi import APIRouter

from .items import router as items_router
from .milestones import router as milestones_router
from .tree import router as tree_router

router = APIRouter()

# Include all sub-routers
router.include_router(tree_router, tags=["portfolio-tree"])
router.include_router(items_router, tags=["portfolio-items"])
router.include_router(milestones_router, tags=["portfolio-milestones"])
