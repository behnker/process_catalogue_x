"""
API v1 router — registers all endpoint groups.
Blueprint §9.7: API endpoint listing.
"""

from fastapi import APIRouter

from src.api.v1.endpoints import auth, business_model, portfolio, processes, riada

api_router = APIRouter()

# Auth (no auth required for login flow)
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Core entities (all require auth)
api_router.include_router(processes.router, prefix="/processes", tags=["Processes"])
api_router.include_router(riada.router, prefix="/riada", tags=["RIADA"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
api_router.include_router(business_model.router, prefix="/business-model", tags=["Business Model"])
