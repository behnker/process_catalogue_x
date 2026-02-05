"""
Issue & Opportunity Log API endpoints.

OPS- prefix for operational issues (distinct from RIADA ISS- project issues).
"""

from fastapi import APIRouter

from .crud import router as crud_router
from .analytics import router as analytics_router
from .export import router as export_router

router = APIRouter()

# Include sub-routers
router.include_router(analytics_router, tags=["issue-analytics"])
router.include_router(export_router, tags=["issue-export"])
router.include_router(crud_router, tags=["issue-crud"])
