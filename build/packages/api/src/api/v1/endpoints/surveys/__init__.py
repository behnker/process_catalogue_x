"""
Survey API endpoints - split into sub-routers.

Blueprint §4.7: 4 survey modes:
  - ai_fluency: AI Fluency Survey (AFI score 0-100)
  - operating_model: Operating Model Survey (SPRD x RAG)
  - change_readiness: Change Readiness Survey (ADKAR-based)
  - adoption_evidence: Adoption Evidence Survey
"""

from fastapi import APIRouter

from .surveys import router as surveys_router
from .questions import router as questions_router
from .responses import router as responses_router

router = APIRouter()

# Include all sub-routers
router.include_router(surveys_router, tags=["surveys"])
router.include_router(questions_router, tags=["survey-questions"])
router.include_router(responses_router, tags=["survey-responses"])
