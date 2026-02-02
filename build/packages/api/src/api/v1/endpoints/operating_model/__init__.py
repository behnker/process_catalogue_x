"""
Operating Model API endpoints - split into sub-routers.

Manages ProcessOperatingModel components per process.

Blueprint §4.4.1: 10 components (SIPOC, RACI, KPIs, Policies, Systems, etc.)
Each component stores Current State and Future State for gap analysis.
"""

from fastapi import APIRouter

from .components import router as components_router
from .summary import router as summary_router

router = APIRouter()

# Include all sub-routers
router.include_router(summary_router, tags=["operating-model-summary"])
router.include_router(components_router, tags=["operating-model-components"])
