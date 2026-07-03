"""Mock-test domain entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class MockTest:
    """A scheduled mock test."""

    day: int
    test_date: date
    name: str
    status: str = "Scheduled"


@dataclass(frozen=True)
class MockAnalysis:
    """Post-mock analysis summary."""

    mock_name: str
    score: int = 0
    accuracy_percentage: int = 0
    key_insight: str = ""
