"""Workbook orchestration for PGPEM Mission Control."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from mission_control.core.config import WorkbookConfig
from .logger import get_logger

if TYPE_CHECKING:
    from mission_control.workbook.base_sheet import BaseSheet


class WorkbookEngine:
    """Facade for building the Mission Control Excel workbook."""

    def __init__(self, config: WorkbookConfig | None = None) -> None:
        self.config = config or WorkbookConfig()
        self.logger = get_logger(__name__)
        self.logger.info("Workbook initialized")

    def build(self, sheets: list[BaseSheet] | None = None) -> Path:
        """Build either the registered custom sheets or the standard workbook."""
        builder = self._create_builder()

        if sheets is None:
            builder.add_standard_workbook()
        else:
            for sheet in sheets:
                builder.register(sheet)

        return builder.build()

    def save(self) -> Path:
        """Build and save the standard workbook."""
        return self.build()

    def _create_builder(self) -> "WorkbookBuilder":
        from mission_control.workbook.builder import WorkbookBuilder

        return WorkbookBuilder(config=self.config)
