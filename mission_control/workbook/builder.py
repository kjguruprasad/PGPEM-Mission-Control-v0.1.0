"""Workbook builder and sheet registry."""

from __future__ import annotations

from pathlib import Path

from mission_control.core.config import WorkbookConfig
from mission_control.core.exceptions import SheetBuildError
from mission_control.core.logger import get_logger
from mission_control.core.workbook_engine import WorkbookEngine
from mission_control.workbook.base_sheet import BaseSheet
from mission_control.workbook.dashboard import DashboardSheet
from mission_control.workbook.sheets import (
    AnalyticsSheet,
    DailyPlannerSheet,
    DilrTrackerSheet,
    HabitsSheet,
    InterviewPrepSheet,
    MockTestsSheet,
    NotesSheet,
    Planner106DaySheet,
    QuantTrackerSheet,
    RevisionTrackerSheet,
    SettingsSheet,
    SmartGoalsSheet,
    STANDARD_SHEET_CLASSES,
    VarcTrackerSheet,
    VocabularySheet,
)


class WorkbookBuilder:
    """Fluent workbook builder with an ordered sheet registry."""

    def __init__(self, config: WorkbookConfig | None = None) -> None:
        self.config = config or WorkbookConfig()
        self.engine = WorkbookEngine(config=self.config)
        self.registry: list[BaseSheet] = []
        self.logger = get_logger(__name__)

    def register(self, sheet: BaseSheet) -> "WorkbookBuilder":
        """Register a sheet instance for inclusion in the workbook."""
        sheet.app_config = self.config.app
        self.registry.append(sheet)
        return self

    def add_dashboard(self) -> "WorkbookBuilder":
        return self.register(DashboardSheet())

    def add_goal_sheet(self) -> "WorkbookBuilder":
        return self.register(SmartGoalsSheet())

    def add_planner(self) -> "WorkbookBuilder":
        return self.register(Planner106DaySheet())

    def add_daily_planner(self) -> "WorkbookBuilder":
        return self.register(DailyPlannerSheet())

    def add_quant_tracker(self) -> "WorkbookBuilder":
        return self.register(QuantTrackerSheet())

    def add_dilr_tracker(self) -> "WorkbookBuilder":
        return self.register(DilrTrackerSheet())

    def add_varc_tracker(self) -> "WorkbookBuilder":
        return self.register(VarcTrackerSheet())

    def add_vocabulary(self) -> "WorkbookBuilder":
        return self.register(VocabularySheet())

    def add_revision_tracker(self) -> "WorkbookBuilder":
        return self.register(RevisionTrackerSheet())

    def add_mock_tests(self) -> "WorkbookBuilder":
        return self.register(MockTestsSheet())

    def add_analytics(self) -> "WorkbookBuilder":
        return self.register(AnalyticsSheet())

    def add_habits(self) -> "WorkbookBuilder":
        return self.register(HabitsSheet())

    def add_notes(self) -> "WorkbookBuilder":
        return self.register(NotesSheet())

    def add_interview_prep(self) -> "WorkbookBuilder":
        return self.register(InterviewPrepSheet())

    def add_settings(self) -> "WorkbookBuilder":
        return self.register(SettingsSheet())

    def add_standard_workbook(self) -> "WorkbookBuilder":
        """Register the complete v0 workbook in product order."""
        self.add_dashboard()
        for sheet_class in STANDARD_SHEET_CLASSES:
            self.register(sheet_class())
        return self

    def build(self) -> Path:
        """Build every registered sheet and save the workbook."""
        self.engine.remove_default_sheet()

        for sheet in self.registry:
            try:
                sheet.attach(self.engine.workbook)
                sheet.build()
            except Exception as exc:  # pragma: no cover - defensive wrapper
                message = f"Failed to build sheet {sheet.title!r}"
                self.logger.exception(message)
                raise SheetBuildError(message) from exc
            self.logger.info("Sheet built: %s", sheet.title)

        return self.engine.save()
