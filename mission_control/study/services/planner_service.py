"""Study planner application service."""

from __future__ import annotations

from dataclasses import dataclass

from mission_control.planner.planner_generator import PlannerGenerator
from mission_control.planner.models import StudyPlanDay
from mission_control.study.repositories import PlannerRepository


@dataclass
class PlannerService:
    """Generate and store study plans."""

    planner_generator: PlannerGenerator
    planner_repository: PlannerRepository

    def generate_plan(self) -> list[StudyPlanDay]:
        """Generate a plan and persist it through the repository."""
        plan = self.planner_generator.generate()
        self.planner_repository.save(plan)
        return plan
