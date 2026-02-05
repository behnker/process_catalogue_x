"""
All SQLAlchemy models — imported here so Alembic can detect them.
"""

from src.models.organization import (
    AllowedDomain,
    AuditLog,
    MagicLinkToken,
    Organization,
    User,
    UserOrganization,
)
from src.models.process import (
    Process,
    ProcessOperatingModel,
)
from src.models.riada import RiadaItem
from src.models.business_model import (
    BusinessModel,
    BusinessModelEntry,
    BusinessModelMapping,
)
from src.models.portfolio import (
    PortfolioItem,
    PortfolioMilestone,
)
from src.models.survey import (
    Survey,
    SurveyQuestion,
    SurveyResponse,
)
from src.models.reference import (
    LLMConfiguration,
    PromptExecution,
    PromptTemplate,
    ReferenceCatalogue,
)
from src.models.system_catalogue import (
    ProcessSystem,
    SystemCatalogue,
)
from src.models.issue_log import (
    IssueLog,
    IssueLogHistory,
)

__all__ = [
    # Organization & Auth
    "Organization",
    "AllowedDomain",
    "User",
    "UserOrganization",
    "MagicLinkToken",
    "AuditLog",
    # Process Spine
    "Process",
    "ProcessOperatingModel",
    # RIADA
    "RiadaItem",
    # Business Model
    "BusinessModel",
    "BusinessModelEntry",
    "BusinessModelMapping",
    # Portfolio
    "PortfolioItem",
    "PortfolioMilestone",
    # Surveys
    "Survey",
    "SurveyQuestion",
    "SurveyResponse",
    # Reference & Prompts
    "ReferenceCatalogue",
    "PromptTemplate",
    "PromptExecution",
    "LLMConfiguration",
    # System Catalogue
    "SystemCatalogue",
    "ProcessSystem",
    # Issue Log
    "IssueLog",
    "IssueLogHistory",
]
