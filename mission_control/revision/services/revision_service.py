"""Revision scheduling service."""

from __future__ import annotations

from dataclasses import dataclass

from mission_control.planner.models import StudyPlanDay
from mission_control.revision.models import RevisionSchedule, RevisionTask


@dataclass(frozen=True)
class RevisionService:
    """Create revision schedules from study plans."""

    def create_schedule(self, plan: list[StudyPlanDay]) -> RevisionSchedule:
        """Return all revision days in the plan."""
        tasks = tuple(
            RevisionTask(
                day=day.day,
                revision_date=day.date,
                label=day.revision,
            )
            for day in plan
            if day.revision
        )
        return RevisionSchedule(tasks=tasks)
