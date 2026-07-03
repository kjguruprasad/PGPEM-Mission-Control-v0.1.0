"""Generic table-backed worksheet implementations."""

from __future__ import annotations

from typing import Any

from mission_control.workbook.base_sheet import BaseSheet


class TableSheet(BaseSheet):
    """A standard worksheet with a title and one formatted table."""

    title: str
    headers: list[str]
    sample_rows: list[tuple[Any, ...]] = []
    header_row = 4

    def build(self) -> None:
        """Build a common titled table sheet."""
        self.prepare_sheet(
            subtitle=f"{self.app_config.exam.name} planning workspace",
        )
        self.write_table(
            self.headers,
            self.sample_rows,
            start_row=self.header_row,
        )
        self.auto_size_columns()
        self._apply_page_setup()

    def _apply_page_setup(self) -> None:
        worksheet = self.worksheet
        worksheet.page_setup.orientation = "landscape"
        worksheet.page_setup.fitToWidth = 1
        worksheet.page_setup.fitToHeight = 0
        worksheet.sheet_properties.pageSetUpPr.fitToPage = True
