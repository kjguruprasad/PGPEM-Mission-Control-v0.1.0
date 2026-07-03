"""Scheduling rules for study hours, revision, and mock tests."""

from __future__ import annotations

from mission_control.core.config import AppConfig
from mission_control.planner.models import CalendarDay, ScheduleSlot


class Scheduler:
    """Apply cadence rules to calendar days."""

    def __init__(self, app_config: AppConfig) -> None:
        self.app_config = app_config

    def schedule(self, calendar_day: CalendarDay) -> ScheduleSlot:
        """Return schedule metadata for a calendar day."""
        study_hours = self._study_hours(calendar_day)
        remaining_days = self.app_config.planner.duration_days - calendar_day.day + 1

        if remaining_days <= 2:
            return ScheduleSlot(
                study_hours=study_hours,
                revision="Light Revision",
                mock_test="",
                revision_only=True,
            )

        if remaining_days <= 7:
            return ScheduleSlot(
                study_hours=study_hours,
                revision="Final Revision",
                mock_test="",
                revision_only=True,
            )

        revision = ""
        if calendar_day.day % self.app_config.revision.every_n_days == 0:
            revision = "Weekly Revision"

        mock_test = ""
        if calendar_day.day % self.app_config.mock.every_n_days == 0:
            mock_number = calendar_day.day // self.app_config.mock.every_n_days
            mock_test = f"Mock Test {mock_number}"

        return ScheduleSlot(
            study_hours=study_hours,
            revision=revision,
            mock_test=mock_test,
            revision_only=False,
        )

    def _study_hours(self, calendar_day: CalendarDay) -> int:
        if calendar_day.is_weekend:
            return self.app_config.study.weekend_hours
        return self.app_config.study.weekday_hours
