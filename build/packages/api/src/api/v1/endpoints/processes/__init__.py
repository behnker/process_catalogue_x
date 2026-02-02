"""
Process Catalogue API endpoints - split into sub-routers.

Full CRUD with hierarchy traversal and tenant isolation.
"""

from fastapi import APIRouter

from .list import router as list_router
from .crud import router as crud_router
from .reorder import router as reorder_router
from .systems import router as systems_router

router = APIRouter()

# Include all sub-routers
router.include_router(list_router, tags=["process-list"])
router.include_router(reorder_router, tags=["process-reorder"])
router.include_router(crud_router, tags=["process-crud"])
router.include_router(systems_router, tags=["process-systems"])
