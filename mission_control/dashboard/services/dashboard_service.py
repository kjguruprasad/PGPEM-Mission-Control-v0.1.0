"""Dashboard data assembly service."""

from __future__ import annotations

from dataclasses import dataclass

from mission_control.mocks.models import MockTest
from mission_control.analytics.models import StudyIntelligenceReport
from mission_control.revision.models import RevisionSchedule
from mission_control.study.services import ProgressMetrics


@dataclass(frozen=True)
class DashboardData:
    """Renderer-neutral dashboard aggregate data."""

    total_study_days: int
    total_study_hours: int
    total_mock_tests: int
    completion_percentage: int
    total_revision_tasks: int
    completed_revisions: int
    pending_revisions: int
    overdue_revisions: int
    revision_completion_percentage: int
    readiness_score: int
    learning_velocity: float
    questions_per_hour: float
    pending_tasks: int
    weak_topics: int
    top_recommendation: str

    @property
    def total_revision_days(self) -> int:
        """Backward-compatible revision count for older workbook checks."""
        return self.total_revision_tasks


@dataclass(frozen=True)
class DashboardService:
    """Build dashboard data from domain service outputs."""

    def build(
        self,
        *,
        progress: ProgressMetrics,
        revision_schedule: RevisionSchedule,
        mock_tests: list[MockTest],
        study_intelligence: StudyIntelligenceReport | None = None,
    ) -> DashboardData:
        """Return dashboard data for renderers."""
        statistics = (
            study_intelligence.statistics
            if study_intelligence is not None
            else None
        )
        velocity = (
            study_intelligence.velocity
            if study_intelligence is not None
            else None
        )
        readiness = (
            study_intelligence.readiness
            if study_intelligence is not None
            else None
        )
        recommendations = (
            study_intelligence.recommendations
            if study_intelligence is not None
            else tuple()
        )
        return DashboardData(
            total_study_days=progress.total_study_days,
            total_study_hours=progress.total_study_hours,
            total_mock_tests=len(mock_tests),
            completion_percentage=progress.completion_percentage,
            total_revision_tasks=revision_schedule.total_due,
            completed_revisions=revision_schedule.completed,
            pending_revisions=(
                revision_schedule.total_due
                - revision_schedule.completed
                - revision_schedule.overdue
            ),
            overdue_revisions=revision_schedule.overdue,
            revision_completion_percentage=self._revision_completion(
                revision_schedule,
            ),
            readiness_score=readiness.score if readiness else 0,
            learning_velocity=velocity.study_hours_per_day if velocity else 0,
            questions_per_hour=velocity.questions_per_hour if velocity else 0,
            pending_tasks=statistics.pending_tasks if statistics else 0,
            weak_topics=(
                len(study_intelligence.weak_topics)
                if study_intelligence is not None
                else 0
            ),
            top_recommendation=(
                recommendations[0].title
                if recommendations
                else "No recommendations yet."
            ),
        )

    @staticmethod
    def _revision_completion(revision_schedule: RevisionSchedule) -> int:
        if revision_schedule.total_due == 0:
            return 0
        return round(
            (revision_schedule.completed / revision_schedule.total_due) * 100,
        )
