"""
Authentication API endpoints - split into sub-routers.

Blueprint §6.2.10 Authentication Endpoints:
  POST /api/v1/auth/magic-link     — Request magic link
  GET  /api/v1/auth/verify/{token} — Verify magic link and login
  POST /api/v1/auth/refresh        — Refresh access token
  POST /api/v1/auth/logout         — Invalidate session
  GET  /api/v1/auth/me             — Current user profile
"""

from fastapi import APIRouter

from .magic_link import router as magic_link_router
from .session import router as session_router

router = APIRouter()

# Include all sub-routers
router.include_router(magic_link_router, tags=["auth-magic-link"])
router.include_router(session_router, tags=["auth-session"])
