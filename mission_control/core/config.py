"""Application configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


PROJECT_NAME = "PGPEM Mission Control"
WORKBOOK_NAME = "PGPEM_Mission_Control.xlsx"
ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_SETTINGS_PATH = ROOT_DIR / "config" / "settings.yaml"


@dataclass(frozen=True)
class ExamConfig:
    """Exam-specific planning settings loaded from YAML."""

    name: str = "IIMB PGPEM"
    days: int = 106


@dataclass(frozen=True)
class AppConfig:
    """Application settings loaded from YAML."""

    project_name: str = PROJECT_NAME
    workbook_name: str = WORKBOOK_NAME
    exam: ExamConfig = field(default_factory=ExamConfig)


def load_app_config(path: Path = DEFAULT_SETTINGS_PATH) -> AppConfig:
    """Load application configuration from YAML with sane defaults."""
    if not path.exists():
        return AppConfig()

    with path.open("r", encoding="utf-8") as settings_file:
        raw_config = yaml.safe_load(settings_file) or {}

    if not isinstance(raw_config, dict):
        return AppConfig()

    exam = _as_mapping(raw_config.get("exam"))
    workbook = _as_mapping(raw_config.get("workbook"))

    return AppConfig(
        project_name=str(raw_config.get("project_name", PROJECT_NAME)),
        workbook_name=str(workbook.get("name", WORKBOOK_NAME)),
        exam=ExamConfig(
            name=str(exam.get("name", "IIMB PGPEM")),
            days=int(exam.get("days", 106)),
        ),
    )


def _as_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


@dataclass(frozen=True)
class WorkbookConfig:
    """Runtime settings for workbook generation."""

    output_dir: Path = ROOT_DIR / "output"
    app: AppConfig = field(default_factory=load_app_config)
    subject: str = "PGPEM preparation dashboard"

    @property
    def output_path(self) -> Path:
        """Return the absolute path where the workbook will be saved."""
        return self.output_dir / self.app.workbook_name

    @property
    def creator(self) -> str:
        """Return the workbook creator metadata."""
        return self.app.project_name

    @property
    def title(self) -> str:
        """Return the workbook title metadata."""
        return self.app.project_name
