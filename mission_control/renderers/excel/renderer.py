"""Excel rendering strategy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mission_control.application.context import ApplicationContext
from mission_control.core.config import WorkbookConfig
from mission_control.workbook.builder import WorkbookBuilder


@dataclass(frozen=True)
class ExcelRenderer:
    """Render application data to the existing Excel workbook target."""

    workbook_config: WorkbookConfig

    def render(self, context: ApplicationContext) -> Path:
        """Generate the Excel workbook from prepared application context."""
        return (
            WorkbookBuilder(config=self.workbook_config)
            .with_context(context)
            .add_standard_workbook()
            .build()
        )
