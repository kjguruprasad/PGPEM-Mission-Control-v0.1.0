"""Progress calculations for study plans."""

from __future__ import annotations

from dataclasses import dataclass

from mission_control.planner.models import StudyPlanDay


@dataclass(frozen=True)
class ProgressMetrics:
    """Dashboard-ready progress metrics."""

    total_study_days: int
    total_study_hours: int
    completion_percentage: int


@dataclass(frozen=True)
class ProgressService:
    """Calculate study progress from plan rows."""

    def calculate(self, plan: list[StudyPlanDay]) -> ProgressMetrics:
        """Return aggregate study progress metrics."""
        total_days = len(plan)
        total_hours = sum(day.study_hours for day in plan)
        completed_days = sum(1 for day in plan if day.status == "Completed")
        completion = round((completed_days / total_days) * 100) if total_days else 0

        return ProgressMetrics(
            total_study_days=total_days,
            total_study_hours=total_hours,
            completion_percentage=completion,
        )
