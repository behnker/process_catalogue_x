"""
Prompt Library API endpoints - split into sub-routers.

Blueprint §4.4.6: Prompt library with templates and execution tracking.
Blueprint §6.4.11: LLM configuration and usage tracking.
"""

from fastapi import APIRouter

from .templates import router as templates_router
from .execution import router as execution_router
from .llm_config import router as llm_config_router

router = APIRouter()

# Include all sub-routers
router.include_router(templates_router, tags=["prompt-templates"])
router.include_router(execution_router, tags=["prompt-execution"])
router.include_router(llm_config_router, tags=["llm-config"])
