"""
RIADA (Quality Logs) API endpoints - split into sub-routers.

Full CRUD with filtering by type, category, severity, status.
"""

from fastapi import APIRouter

from .items import router as items_router
from .summary import router as summary_router

router = APIRouter()

# Include all sub-routers
router.include_router(summary_router, tags=["riada-summary"])
router.include_router(items_router, tags=["riada-items"])
