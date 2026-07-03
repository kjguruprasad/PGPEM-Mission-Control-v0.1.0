"""Learning velocity model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class LearningVelocity:
    """Velocity and projection metrics."""

    study_hours_per_day: float
    questions_per_day: float
    questions_per_hour: float
    average_completion_rate: float
    projected_completion_date: date | None
