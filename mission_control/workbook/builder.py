"""Workbook builder and sheet registry."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from openpyxl import Workbook

from mission_control.core.config import WorkbookConfig
from mission_control.core.exceptions import SheetBuildError
from mission_control.core.logger import get_logger
from mission_control.planner.planner_generator import PlannerGenerator
from mission_control.workbook.base_sheet import BaseSheet
from mission_control.workbook.dashboard import DashboardSheet
from mission_control.workbook.sheets import (
    AnalyticsSheet,
    DailyPlannerSheet,
    DILRTrackerSheet,
    HabitsSheet,
    InterviewPrepSheet,
    MockTestSheet,
    NotesSheet,
    Planner106Sheet,
    QuantTrackerSheet,
    RevisionSheet,
    SettingsSheet,
    SmartGoalsSheet,
    VARCTrackerSheet,
    VocabularySheet,
)

if TYPE_CHECKING:
    from mission_control.application.context import ApplicationContext


class WorkbookBuilder:
    """Fluent workbook builder with an ordered sheet registry."""

    def __init__(self, config: WorkbookConfig | None = None) -> None:
        self.config = config or WorkbookConfig()
        self.workbook = Workbook()
        self.registry: list[BaseSheet] = []
        self.logger = get_logger(__name__)
        self.context: ApplicationContext | None = None
        self.planner_generator = PlannerGenerator.from_app_config(
            app_config=self.config.app,
        )
        self._configure_properties()

    def with_context(self, context: "ApplicationContext") -> "WorkbookBuilder":
        """Inject renderer-neutral application data into workbook sheets."""
        self.context = context
        return self

    def register(self, sheet: BaseSheet) -> "WorkbookBuilder":
        """Register a sheet instance for inclusion in the workbook."""
        sheet.app_config = self.config.app
        sheet.context = self.context
        self.registry.append(sheet)
        return self

    def add_dashboard(self) -> "WorkbookBuilder":
        return self.register(
            DashboardSheet(planner_generator=self.planner_generator),
        )

    def add_goal_sheet(self) -> "WorkbookBuilder":
        return self.register(SmartGoalsSheet())

    def add_planner(self) -> "WorkbookBuilder":
        return self.register(
            Planner106Sheet(planner_generator=self.planner_generator),
        )

    def add_daily_planner(self) -> "WorkbookBuilder":
        return self.register(DailyPlannerSheet())

    def add_quant_tracker(self) -> "WorkbookBuilder":
        return self.register(QuantTrackerSheet())

    def add_dilr_tracker(self) -> "WorkbookBuilder":
        return self.register(DILRTrackerSheet())

    def add_varc_tracker(self) -> "WorkbookBuilder":
        return self.register(VARCTrackerSheet())

    def add_vocabulary(self) -> "WorkbookBuilder":
        return self.register(VocabularySheet())

    def add_revision_tracker(self) -> "WorkbookBuilder":
        return self.register(RevisionSheet())

    def add_mock_tests(self) -> "WorkbookBuilder":
        return self.register(MockTestSheet())

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
        self.add_goal_sheet()
        self.add_planner()
        self.add_daily_planner()
        self.add_quant_tracker()
        self.add_dilr_tracker()
        self.add_varc_tracker()
        self.add_vocabulary()
        self.add_revision_tracker()
        self.add_mock_tests()
        self.add_analytics()
        self.add_habits()
        self.add_notes()
        self.add_interview_prep()
        self.add_settings()
        return self

    def build(self) -> Path:
        """Build every registered sheet and save the workbook."""
        self._remove_default_sheet()

        for sheet in self.registry:
            try:
                sheet.attach(self.workbook)
                sheet.build()
            except Exception as exc:  # pragma: no cover - defensive wrapper
                message = f"Failed to build sheet {sheet.title!r}"
                self.logger.exception(message)
                raise SheetBuildError(message) from exc
            self.logger.info("Sheet built: %s", sheet.title)

        return self.save()

    def save(self) -> Path:
        """Save the generated workbook and return the output path."""
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.config.output_path
        self.workbook.save(output_path)
        self.logger.info("Workbook saved to %s", output_path)
        return output_path

    def _remove_default_sheet(self) -> None:
        sheet = self.workbook.active
        if sheet and sheet.title == "Sheet":
            self.workbook.remove(sheet)

    def _configure_properties(self) -> None:
        self.workbook.properties.creator = self.config.creator
        self.workbook.properties.title = self.config.title
        self.workbook.properties.subject = self.config.subject
