"""Calendar generation for the 106-day planner."""

from __future__ import annotations

from datetime import date, timedelta

from mission_control.planner.models import CalendarDay


class CalendarGenerator:
    """Generate the dated study-plan calendar."""

    def __init__(self, *, exam_date: date, duration_days: int) -> None:
        self.exam_date = exam_date
        self.duration_days = duration_days

    @property
    def start_date(self) -> date:
        """Return the first planner date."""
        return self.exam_date - timedelta(days=self.duration_days)

    @property
    def end_date(self) -> date:
        """Return the final planner date before the exam."""
        return self.exam_date - timedelta(days=1)

    def generate(self) -> list[CalendarDay]:
        """Generate one calendar day per planner day."""
        return [
            CalendarDay(
                day=day_number,
                date=self.start_date + timedelta(days=day_number - 1),
            )
            for day_number in range(1, self.duration_days + 1)
        ]
