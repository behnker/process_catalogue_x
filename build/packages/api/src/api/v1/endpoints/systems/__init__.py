"""
System Catalogue API endpoints.

Blueprint §9.6.9: System registry with process linkages.
"""

from fastapi import APIRouter

from .items import router as items_router
from .mutations import router as mutations_router
from .processes import router as processes_router

router = APIRouter()

# System read (list, get)
router.include_router(items_router, tags=["systems"])
# System write (create, update, delete)
router.include_router(mutations_router, tags=["systems"])
# Process-System linkages
router.include_router(processes_router, tags=["systems-processes"])
