"""Application configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PROJECT_NAME = "PGPEM Mission Control"
WORKBOOK_NAME = "PGPEM_Mission_Control.xlsx"
ROOT_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class WorkbookConfig:
    """Runtime settings for workbook generation."""

    output_dir: Path = ROOT_DIR / "output"
    workbook_name: str = WORKBOOK_NAME
    creator: str = PROJECT_NAME
    subject: str = "PGPEM preparation dashboard"
    title: str = PROJECT_NAME

    @property
    def output_path(self) -> Path:
        """Return the absolute path where the workbook will be saved."""
        return self.output_dir / self.workbook_name
