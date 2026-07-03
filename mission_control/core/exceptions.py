"""Custom exceptions for Mission Control."""

from __future__ import annotations


class MissionControlError(Exception):
    """Base exception for application-specific failures."""


class WorkbookGenerationError(MissionControlError):
    """Raised when workbook generation fails."""


class SheetBuildError(WorkbookGenerationError):
    """Raised when a workbook sheet cannot be built."""
