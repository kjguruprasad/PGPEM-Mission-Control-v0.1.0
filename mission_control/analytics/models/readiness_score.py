"""Readiness score model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReadinessScore:
    """Weighted readiness score."""

    score: int
    completion_weight: int
    revision_weight: int
    consistency_weight: int
    mock_weight: int
    confidence_weight: int
