"""
Operating Model API endpoints - split into sub-routers.

Manages ProcessOperatingModel JSONB components (resources, security, data)
and dedicated relational tables (RACI, KPIs, Governance, Policies, Timing, SIPOC).
Systems is served by the system_catalogue module.

Blueprint §4.4.1: 10 components total.
"""

from fastapi import APIRouter

from .components import router as components_router
from .governance import router as governance_router
from .kpis import router as kpis_router
from .policies import router as policies_router
from .raci import router as raci_router
from .roles import router as roles_router
from .sipoc import router as sipoc_router
from .summary import router as summary_router
from .timing import router as timing_router

router = APIRouter()

# Summary + JSONB components
router.include_router(summary_router, tags=["operating-model-summary"])
router.include_router(components_router, tags=["operating-model-components"])

# Relational component endpoints
router.include_router(raci_router, tags=["operating-model-raci"])
router.include_router(kpis_router, tags=["operating-model-kpis"])
router.include_router(governance_router, tags=["operating-model-governance"])
router.include_router(policies_router, tags=["operating-model-policies"])
router.include_router(timing_router, tags=["operating-model-timing"])
router.include_router(sipoc_router, tags=["operating-model-sipoc"])

# Reference data
router.include_router(roles_router, tags=["operating-model-roles"])
