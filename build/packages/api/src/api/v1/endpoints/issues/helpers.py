"""Shared helpers for issue endpoints."""

from fastapi import HTTPException

from src.models.issue_log import IssueLog
from src.schemas.issue_log import IssueResponse


def level_to_int(level_str: str) -> int:
    """Convert 'L0'-'L5' to 0-5."""
    return int(level_str[1]) if level_str and level_str.startswith("L") else 0


def validate_status_transition(current: str, new: str) -> None:
    """Validate issue status transitions per spec BR-01 through BR-10."""
    allowed = {
        "open": {"in_progress", "deferred", "closed"},
        "in_progress": {"resolved", "deferred", "open"},
        "resolved": {"closed", "in_progress"},
        "deferred": {"open", "closed"},
        "closed": set(),  # Terminal state
    }

    if new not in allowed.get(current, set()):
        raise HTTPException(
            status_code=422,
            detail=f"Cannot transition from '{current}' to '{new}'",
        )


def to_response(issue: IssueLog) -> IssueResponse:
    """Convert IssueLog model to response schema."""
    return IssueResponse(
        id=issue.id,
        display_id=issue.display_id,
        issue_number=issue.issue_number,
        title=issue.title,
        description=issue.description,
        issue_classification=issue.issue_classification,
        issue_criticality=issue.issue_criticality,
        issue_complexity=issue.issue_complexity,
        issue_status=issue.issue_status,
        process_id=issue.process_id,
        process_level=issue.process_level,
        process_ref=issue.process_ref,
        process_name=issue.process_name,
        raised_by_id=issue.raised_by_id,
        assigned_to_id=issue.assigned_to_id,
        date_raised=issue.date_raised,
        target_resolution_date=issue.target_resolution_date,
        actual_resolution_date=issue.actual_resolution_date,
        resolution_summary=issue.resolution_summary,
        opportunity_flag=issue.opportunity_flag,
        opportunity_status=issue.opportunity_status,
        opportunity_description=issue.opportunity_description,
        opportunity_expected_benefit=issue.opportunity_expected_benefit,
        opportunity_beneficiary_roles=issue.opportunity_beneficiary_roles or [],
        created_by=issue.created_by,
        updated_by=issue.updated_by,
        created_at=issue.created_at,
        updated_at=issue.updated_at,
    )
