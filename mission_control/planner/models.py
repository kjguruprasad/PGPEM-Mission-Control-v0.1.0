"""Planner domain models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Topic:
    """A study topic with allocation weight."""

    name: str
    weight: int = 1


@dataclass(frozen=True)
class CalendarDay:
    """A dated planner day."""

    day: int
    date: date

    @property
    def week(self) -> int:
        """Return the 1-indexed planner week number."""
        return ((self.day - 1) // 7) + 1

    @property
    def day_of_week(self) -> str:
        """Return the weekday name."""
        return self.date.strftime("%A")

    @property
    def is_weekend(self) -> bool:
        """Return whether this date is Saturday or Sunday."""
        return self.date.weekday() >= 5


@dataclass(frozen=True)
class ScheduleSlot:
    """Schedule metadata for a planner day."""

    study_hours: int
    revision: str
    mock_test: str
    revision_only: bool


@dataclass(frozen=True)
class StudyPlanDay:
    """A complete daily study plan row."""

    day: int
    date: date
    week: int
    day_of_week: str
    quant_topic: str
    dilr_topic: str
    varc_topic: str
    revision: str
    mock_test: str
    study_hours: int
    status: str = "Not Started"
    notes: str = ""
