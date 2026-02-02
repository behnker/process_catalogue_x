"""
API v1 router — registers all endpoint groups.
Blueprint §9.7: API endpoint listing.
"""

from fastapi import APIRouter

from src.api.v1.endpoints import (
    auth,
    business_model,
    operating_model,
    portfolio,
    processes,
    prompts,
    reference,
    riada,
    surveys,
)

api_router = APIRouter()

# Auth (no auth required for login flow)
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Core entities (all require auth)
api_router.include_router(processes.router, prefix="/processes", tags=["Processes"])
api_router.include_router(
    operating_model.router, prefix="/processes", tags=["Operating Model"]
)
api_router.include_router(riada.router, prefix="/riada", tags=["RIADA"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
api_router.include_router(business_model.router, prefix="/business-model", tags=["Business Model"])

# Reference data
api_router.include_router(reference.router, prefix="/reference", tags=["Reference Data"])

# Phase 2 features
api_router.include_router(surveys.router, prefix="/surveys", tags=["Surveys"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["Prompt Library"])
