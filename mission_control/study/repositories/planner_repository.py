"""Planner repository abstractions."""

from __future__ import annotations

from dataclasses import dataclass, field

from mission_control.planner.models import StudyPlanDay


@dataclass
class PlannerRepository:
    """In-memory planner repository for generated plans."""

    _plan: list[StudyPlanDay] = field(default_factory=list)

    def save(self, plan: list[StudyPlanDay]) -> None:
        """Persist the generated plan in memory."""
        self._plan = list(plan)

    def list(self) -> list[StudyPlanDay]:
        """Return stored planner rows."""
        return list(self._plan)
