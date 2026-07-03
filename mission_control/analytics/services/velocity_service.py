"""Learning velocity service."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from mission_control.analytics.models import LearningVelocity, StudyStatistics


@dataclass(frozen=True)
class VelocityService:
    """Calculate learning velocity and projections."""

    def calculate(
        self,
        statistics: StudyStatistics,
        *,
        elapsed_days: int,
        total_questions: int = 0,
    ) -> LearningVelocity:
        """Return learning velocity metrics."""
        safe_elapsed_days = max(elapsed_days, 1)
        study_hours_per_day = statistics.completed_hours / safe_elapsed_days
        questions_per_day = total_questions / safe_elapsed_days
        questions_per_hour = (
            total_questions / statistics.completed_hours
            if statistics.completed_hours
            else 0
        )
        average_completion_rate = (
            statistics.completed_tasks / safe_elapsed_days
            if safe_elapsed_days
            else 0
        )
        projected_completion_date = self._project_completion_date(
            statistics,
            study_hours_per_day,
        )

        return LearningVelocity(
            study_hours_per_day=round(study_hours_per_day, 2),
            questions_per_day=round(questions_per_day, 2),
            questions_per_hour=round(questions_per_hour, 2),
            average_completion_rate=round(average_completion_rate, 2),
            projected_completion_date=projected_completion_date,
        )

    @staticmethod
    def _project_completion_date(
        statistics: StudyStatistics,
        study_hours_per_day: float,
    ) -> date | None:
        remaining_hours = statistics.total_hours - statistics.completed_hours
        if remaining_hours <= 0:
            return date.today()
        if study_hours_per_day <= 0:
            return None
        days_remaining = round(remaining_hours / study_hours_per_day)
        return date.today() + timedelta(days=max(days_remaining, 1))
