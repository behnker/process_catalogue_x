"""Common schemas for pagination, errors, and health."""

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field, field_validator

# Backward-compatible re-exports
from src.schemas.business_model import (  # noqa: F401
    BusinessModelCanvasResponse,
    BusinessModelEntryCreate,
    BusinessModelEntryResponse,
)

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standard paginated response format.

    Matches frontend PaginatedResponse<T> interface.
    """
    items: list[T]
    total: int = Field(..., ge=0, description="Total number of items across all pages")
    page: int = Field(1, ge=1, description="Current page number (1-indexed)")
    per_page: int = Field(50, ge=1, le=100, description="Items per page")
    has_more: bool = Field(..., description="Whether more pages exist")

    @field_validator("has_more", mode="before")
    @classmethod
    def compute_has_more(cls, v, info):
        """Auto-compute has_more if not provided."""
        if v is not None:
            return v
        total = info.data.get("total", 0)
        page = info.data.get("page", 1)
        per_page = info.data.get("per_page", 50)
        return (page * per_page) < total

    @property
    def total_pages(self) -> int:
        """Calculate total pages."""
        if self.per_page <= 0:
            return 0
        return (self.total + self.per_page - 1) // self.per_page


class ErrorDetail(BaseModel):
    """Detail about a specific error."""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None


class ErrorResponse(BaseModel):
    """
    Standard error response format.

    Consistent format across all endpoints for error handling.
    """
    error: dict[str, Any] = Field(
        ...,
        description="Error details",
        examples=[{
            "code": "VALIDATION_ERROR",
            "message": "Invalid input data",
            "details": [{"field": "name", "message": "Name is required"}]
        }]
    )

    @classmethod
    def create(
        cls,
        code: str,
        message: str,
        details: Optional[list[dict[str, Any]]] = None
    ) -> "ErrorResponse":
        """Factory method to create an error response."""
        return cls(
            error={
                "code": code,
                "message": message,
                "details": details or []
            }
        )


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str
    environment: str
