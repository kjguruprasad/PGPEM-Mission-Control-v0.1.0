"""Concrete workbook sheet definitions."""

from __future__ import annotations

from datetime import date
from typing import Any

from openpyxl.styles import Alignment

from mission_control.planner.planner_generator import PlannerGenerator
from mission_control.workbook.table_sheet import TableSheet


class SmartGoalsSheet(TableSheet):
    title = "SMART Goals"
    headers = ["Goal", "Specific Outcome", "Metric", "Target Date", "Status"]
    sample_rows = [
        ("Quant accuracy", "Improve arithmetic accuracy", "85%", "Day 45", "Planned"),
        (
            "Mock readiness",
            "Complete full mock review loop",
            "10 mocks",
            "Day 90",
            "Planned",
        ),
    ]


class Planner106Sheet(TableSheet):
    title = "106-Day Planner"
    headers = [
        "Day",
        "Date",
        "Week",
        "Day of Week",
        "Quant Topic",
        "DILR Topic",
        "VARC Topic",
        "Revision",
        "Mock Test",
        "Study Hours",
        "Status",
        "Notes",
    ]

    def __init__(
        self,
        *,
        planner_generator: PlannerGenerator | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.planner_generator = planner_generator

    def build(self) -> None:
        """Build the fully populated 106-day planner worksheet."""
        self.prepare_sheet(
            subtitle=(
                f"{self.app_config.exam.name} | "
                f"Exam Date: {self.app_config.exam.exam_date:%d %b %Y}"
            ),
        )
        plan = self._planner_generator().generate()
        rows = [
            (
                plan_day.day,
                plan_day.date,
                plan_day.week,
                plan_day.day_of_week,
                plan_day.quant_topic,
                plan_day.dilr_topic,
                plan_day.varc_topic,
                plan_day.revision,
                plan_day.mock_test,
                plan_day.study_hours,
                plan_day.status,
                plan_day.notes,
            )
            for plan_day in plan
        ]
        end_row, end_column = self.write_table(
            self.headers,
            rows,
            start_row=self.header_row,
        )
        self.freeze_header_row(self.header_row)
        self.apply_auto_filter(
            start_row=self.header_row,
            start_column=1,
            end_row=end_row,
            end_column=end_column,
        )
        self.apply_alternating_rows(
            start_row=self.header_row + 1,
            end_row=end_row,
            start_column=1,
            end_column=end_column,
        )
        self._format_plan_rows(end_row)
        self.auto_size_columns()
        self._apply_page_setup()

    def _planner_generator(self) -> PlannerGenerator:
        if self.planner_generator is None:
            self.planner_generator = PlannerGenerator.from_app_config(
                app_config=self.app_config,
            )
        return self.planner_generator

    def _format_plan_rows(self, end_row: int) -> None:
        for row in range(self.header_row + 1, end_row + 1):
            date_cell = self.worksheet.cell(row=row, column=2)
            if isinstance(date_cell.value, date):
                date_cell.number_format = "yyyy-mm-dd"

            for column in (1, 3, 10):
                self.worksheet.cell(row=row, column=column).alignment = Alignment(
                    horizontal="center",
                    vertical="center",
                )


class DailyPlannerSheet(TableSheet):
    title = "Daily Planner"
    headers = ["Date", "Available Time", "Priority 1", "Priority 2", "Review", "Energy"]
    sample_rows = [
        ("", "90 min", "Quant drills", "Vocabulary", "Error log", "Medium"),
        ("", "60 min", "VARC passage", "Formula revision", "Notes", "High"),
    ]


class QuantTrackerSheet(TableSheet):
    title = "Quant Tracker"
    headers = [
        "Topic",
        "Concept",
        "Practice Sets",
        "Accuracy %",
        "Weak Area",
        "Next Review",
    ]
    sample_rows = [
        ("Arithmetic", "Percentages", 3, 78, "Speed", ""),
        ("Algebra", "Linear equations", 2, 72, "Setup", ""),
    ]


class DILRTrackerSheet(TableSheet):
    title = "DILR Tracker"
    headers = [
        "Set Type",
        "Sets Attempted",
        "Solved",
        "Avg Time",
        "Accuracy %",
        "Notes",
    ]
    sample_rows = [
        ("Arrangements", 4, 3, "14 min", 75, "Improve diagramming"),
        ("Tables", 3, 2, "16 min", 67, "Reduce rereads"),
    ]


class VARCTrackerSheet(TableSheet):
    title = "VARC Tracker"
    headers = ["Area", "Passages/Questions", "Accuracy %", "Review Theme", "Next Drill"]
    sample_rows = [
        ("Reading Comprehension", 3, 70, "Inference errors", "Dense passages"),
        ("Para Summary", 10, 80, "Option traps", "Timed set"),
    ]


class VocabularySheet(TableSheet):
    title = "Vocabulary"
    headers = ["Word", "Meaning", "Example", "Source", "Revision Count", "Confidence"]
    sample_rows = [
        (
            "Abate",
            "Reduce in intensity",
            "The pressure began to abate.",
            "Reading",
            1,
            "Medium",
        ),
        (
            "Lucid",
            "Clear and easy to understand",
            "A lucid explanation.",
            "Article",
            2,
            "High",
        ),
    ]


class RevisionSheet(TableSheet):
    title = "Revision Tracker"
    headers = ["Topic", "Revision 1", "Revision 2", "Revision 3", "Retention", "Action"]
    sample_rows = [
        ("Number systems", "", "", "", "Medium", "Rework errors"),
        ("Grammar rules", "", "", "", "High", "Maintain"),
    ]


class MockTestSheet(TableSheet):
    title = "Mock Tests"
    headers = ["Mock", "Date", "Score", "Percentile", "Accuracy %", "Top Insight"]
    sample_rows = [
        ("Mock 1", "", 0, "", 0, "Capture baseline"),
        ("Mock 2", "", 0, "", 0, "Compare strategy"),
    ]


class AnalyticsSheet(TableSheet):
    title = "Analytics"
    headers = ["Metric", "Current", "Target", "Trend", "Interpretation"]
    sample_rows = [
        ("Weekly hours", 18, 20, "Up", "Close to target"),
        ("Mock accuracy", "68%", "80%", "Flat", "Needs review depth"),
    ]


class HabitsSheet(TableSheet):
    title = "Habits"
    headers = ["Habit", "Frequency", "Trigger", "Streak", "Status"]
    sample_rows = [
        ("Vocabulary review", "Daily", "After breakfast", 9, "Active"),
        ("Error log review", "3x/week", "After practice", 2, "Active"),
    ]


class NotesSheet(TableSheet):
    title = "Notes"
    headers = ["Date", "Category", "Note", "Linked Topic", "Follow-up"]
    sample_rows = [
        (
            "",
            "Strategy",
            "Review every incorrect mock question.",
            "Mock Tests",
            "Weekly",
        ),
        ("", "Mindset", "Protect deep work blocks.", "Habits", "Daily"),
    ]


class InterviewPrepSheet(TableSheet):
    title = "Interview Prep"
    headers = ["Area", "Prompt", "Draft Status", "Evidence", "Next Step"]
    sample_rows = [
        ("SOP", "Why PGPEM?", "Draft", "Career goals", "Refine narrative"),
        (
            "STAR Story",
            "Leadership challenge",
            "Outline",
            "Project example",
            "Add metrics",
        ),
    ]


class SettingsSheet(TableSheet):
    title = "Settings"
    headers = ["Setting", "Value", "Source", "Notes"]

    @property
    def sample_rows(self) -> list[tuple[str, str | int, str, str]]:
        return [
            ("Project", self.app_config.project_name, "YAML", "Workbook title"),
            ("Exam", self.app_config.exam.name, "YAML", "Target program"),
            (
                "Exam Date",
                self.app_config.exam.exam_date.isoformat(),
                "YAML",
                "Used by planner",
            ),
            (
                "Plan Days",
                self.app_config.planner.duration_days,
                "YAML",
                "Used by planner",
            ),
            (
                "Weekday Hours",
                self.app_config.study.weekday_hours,
                "YAML",
                "Used by scheduler",
            ),
            (
                "Weekend Hours",
                self.app_config.study.weekend_hours,
                "YAML",
                "Used by scheduler",
            ),
            (
                "Revision Cadence",
                self.app_config.revision.every_n_days,
                "YAML",
                "Days",
            ),
            (
                "Mock Cadence",
                self.app_config.mock.every_n_days,
                "YAML",
                "Days",
            ),
        ]


STANDARD_SHEET_CLASSES = [
    SmartGoalsSheet,
    Planner106Sheet,
    DailyPlannerSheet,
    QuantTrackerSheet,
    DILRTrackerSheet,
    VARCTrackerSheet,
    VocabularySheet,
    RevisionSheet,
    MockTestSheet,
    AnalyticsSheet,
    HabitsSheet,
    NotesSheet,
    InterviewPrepSheet,
    SettingsSheet,
]
