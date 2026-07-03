"""Reusable openpyxl styling helpers."""

from __future__ import annotations

from collections.abc import Mapping

from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.worksheet import Worksheet

from mission_control.core.theme import Theme


def solid_fill(color: str) -> PatternFill:
    """Create a solid fill from a hex color without a leading hash."""
    return PatternFill(fill_type="solid", fgColor=color)


def thin_border(color: str) -> Border:
    """Return a thin border for table cells."""
    side = Side(style="thin", color=color)
    return Border(left=side, right=side, top=side, bottom=side)


def apply_table_header_style(
    worksheet: Worksheet,
    row: int,
    start_column: int,
    end_column: int,
    theme: Theme,
) -> None:
    """Apply the standard table header style to a contiguous row range."""
    for column in range(start_column, end_column + 1):
        cell = worksheet.cell(row=row, column=column)
        cell.fill = solid_fill(theme.primary)
        cell.font = Font(
            name=theme.header_font,
            size=theme.header_size,
            bold=True,
            color=theme.white,
        )
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border(theme.border)


def apply_column_widths(
    worksheet: Worksheet,
    widths: Mapping[str, float],
) -> None:
    """Apply explicit widths to worksheet columns."""
    for column, width in widths.items():
        worksheet.column_dimensions[column].width = width
