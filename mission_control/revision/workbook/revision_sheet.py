"""Revision planner workbook sheet."""

from __future__ import annotations

from datetime import date

from openpyxl.styles import Alignment

from mission_control.revision.models import RevisionTask
from mission_control.workbook.table_sheet import TableSheet


class RevisionPlannerSheet(TableSheet):
    """Render revision tasks without calculating revision business logic."""

    title = "Revision Planner"
    headers = [
        "Revision ID",
        "Study Task",
        "Topic",
        "Revision Number",
        "Scheduled Date",
        "Status",
        "Completed",
        "Completed Date",
        "Notes",
    ]

    def build(self) -> None:
        """Build the revision planner worksheet."""
        self.prepare_sheet(subtitle="Spaced repetition revision schedule")
        revision_tasks = self._revision_tasks()
        rows = [
            (
                task.id,
                task.study_task_id,
                task.topic,
                task.revision_number,
                task.scheduled_date,
                task.status.value,
                "Yes" if task.completed else "No",
                task.completed_date,
                task.notes,
            )
            for task in revision_tasks
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
        self._format_rows(end_row)
        self.auto_size_columns()
        self._apply_page_setup()

    def _revision_tasks(self) -> tuple[RevisionTask, ...]:
        if self.context is None:
            return tuple()
        return self.context.revision_schedule.revision_tasks

    def _format_rows(self, end_row: int) -> None:
        for row in range(self.header_row + 1, end_row + 1):
            for column in (4, 7):
                self.worksheet.cell(row=row, column=column).alignment = Alignment(
                    horizontal="center",
                    vertical="center",
                )

            for column in (5, 8):
                cell = self.worksheet.cell(row=row, column=column)
                if isinstance(cell.value, date):
                    cell.number_format = "yyyy-mm-dd"
