"""Study statistics model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StudyStatistics:
    """Aggregate study-task statistics."""

    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
    total_hours: int
    completed_hours: int
    completion_percentage: int
    revision_completion_percentage: int
