"""Renderer protocol."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from mission_control.application.context import ApplicationContext


class Renderer(Protocol):
    """Strategy interface for application renderers."""

    def render(self, context: ApplicationContext) -> Path:
        """Render an application context."""
