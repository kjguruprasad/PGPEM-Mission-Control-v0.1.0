"""Mock-test service."""

from __future__ import annotations

from dataclasses import dataclass

from mission_control.mocks.models import MockTest
from mission_control.planner.models import StudyPlanDay


@dataclass(frozen=True)
class MockService:
    """Create mock-test schedules from study plans."""

    def create_mock_tests(self, plan: list[StudyPlanDay]) -> list[MockTest]:
        """Return scheduled mock tests."""
        return [
            MockTest(
                day=day.day,
                test_date=day.date,
                name=day.mock_test,
            )
            for day in plan
            if day.mock_test
        ]
