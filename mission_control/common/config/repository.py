"""Configuration repository adapters."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mission_control.core.config import (
    DEFAULT_SETTINGS_PATH,
    AppConfig,
    load_app_config,
)


@dataclass(frozen=True)
class ConfigurationRepository:
    """Load application configuration from persistent storage."""

    settings_path: Path = DEFAULT_SETTINGS_PATH

    def load(self) -> AppConfig:
        """Return the typed application configuration."""
        return load_app_config(self.settings_path)
