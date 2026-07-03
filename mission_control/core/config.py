"""Application configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
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

    name: str = "IIM Bangalore PGPEM"
    exam_date: date = date(2026, 10, 17)
    days: int = 106


@dataclass(frozen=True)
class PlannerConfig:
    """Planner horizon settings."""

    duration_days: int = 106


@dataclass(frozen=True)
class StudyConfig:
    """Study-hour settings for weekdays and weekends."""

    weekday_hours: int = 3
    weekend_hours: int = 6


@dataclass(frozen=True)
class RevisionConfig:
    """Revision cadence settings."""

    every_n_days: int = 7


@dataclass(frozen=True)
class MockConfig:
    """Mock-test cadence settings."""

    every_n_days: int = 14


@dataclass(frozen=True)
class AppConfig:
    """Application settings loaded from YAML."""

    project_name: str = PROJECT_NAME
    workbook_name: str = WORKBOOK_NAME
    exam: ExamConfig = field(default_factory=ExamConfig)
    planner: PlannerConfig = field(default_factory=PlannerConfig)
    study: StudyConfig = field(default_factory=StudyConfig)
    revision: RevisionConfig = field(default_factory=RevisionConfig)
    mock: MockConfig = field(default_factory=MockConfig)


def load_app_config(path: Path = DEFAULT_SETTINGS_PATH) -> AppConfig:
    """Load application configuration from YAML with sane defaults."""
    if not path.exists():
        return AppConfig()

    with path.open("r", encoding="utf-8") as settings_file:
        raw_config = yaml.safe_load(settings_file) or {}

    if not isinstance(raw_config, dict):
        return AppConfig()

    exam = _as_mapping(raw_config.get("exam"))
    planner = _as_mapping(raw_config.get("planner"))
    study = _as_mapping(raw_config.get("study"))
    revision = _as_mapping(raw_config.get("revision"))
    mock = _as_mapping(raw_config.get("mock"))
    workbook = _as_mapping(raw_config.get("workbook"))
    duration_days = int(planner.get("duration_days", 106))

    return AppConfig(
        project_name=str(raw_config.get("project_name", PROJECT_NAME)),
        workbook_name=str(workbook.get("name", WORKBOOK_NAME)),
        exam=ExamConfig(
            name=str(exam.get("name", "IIM Bangalore PGPEM")),
            exam_date=_parse_date(exam.get("exam_date"), date(2026, 10, 17)),
            days=int(exam.get("days", duration_days)),
        ),
        planner=PlannerConfig(duration_days=duration_days),
        study=StudyConfig(
            weekday_hours=int(study.get("weekday_hours", 3)),
            weekend_hours=int(study.get("weekend_hours", 6)),
        ),
        revision=RevisionConfig(
            every_n_days=int(revision.get("every_n_days", 7)),
        ),
        mock=MockConfig(
            every_n_days=int(mock.get("every_n_days", 14)),
        ),
    )


def _as_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _parse_date(value: Any, default: date) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    return default


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
