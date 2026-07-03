"""Recommendation model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Recommendation:
    """Actionable study recommendation."""

    title: str
    description: str
    priority: str
    category: str
    generated_date: date
