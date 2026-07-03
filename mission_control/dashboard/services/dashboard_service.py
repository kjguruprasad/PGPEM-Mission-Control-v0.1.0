"""Dashboard data assembly service."""

from __future__ import annotations

from dataclasses import dataclass

from mission_control.mocks.models import MockTest
from mission_control.revision.models import RevisionSchedule
from mission_control.study.services import ProgressMetrics


@dataclass(frozen=True)
class DashboardData:
    """Renderer-neutral dashboard aggregate data."""

    total_study_days: int
    total_study_hours: int
    total_revision_days: int
    total_mock_tests: int
    completion_percentage: int


@dataclass(frozen=True)
class DashboardService:
    """Build dashboard data from domain service outputs."""

    def build(
        self,
        *,
        progress: ProgressMetrics,
        revision_schedule: RevisionSchedule,
        mock_tests: list[MockTest],
    ) -> DashboardData:
        """Return dashboard data for renderers."""
        return DashboardData(
            total_study_days=progress.total_study_days,
            total_study_hours=progress.total_study_hours,
            total_revision_days=len(revision_schedule.tasks),
            total_mock_tests=len(mock_tests),
            completion_percentage=progress.completion_percentage,
        )
