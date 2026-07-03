"""Readiness scoring service."""

from __future__ import annotations

from dataclasses import dataclass

from mission_control.analytics.models import ReadinessScore, StudyStatistics
from mission_control.core.config import ReadinessWeightsConfig


@dataclass(frozen=True)
class ReadinessService:
    """Calculate weighted readiness scores."""

    weights: ReadinessWeightsConfig

    def calculate(
        self,
        statistics: StudyStatistics,
        *,
        consistency_score: int = 0,
        mock_score: int = 0,
        confidence_score: int = 0,
    ) -> ReadinessScore:
        """Return a weighted readiness score."""
        weighted_score = (
            statistics.completion_percentage * self.weights.completion
            + statistics.revision_completion_percentage * self.weights.revision
            + consistency_score * self.weights.consistency
            + mock_score * self.weights.mock
            + confidence_score * self.weights.confidence
        ) / self._total_weight()

        return ReadinessScore(
            score=round(weighted_score),
            completion_weight=self.weights.completion,
            revision_weight=self.weights.revision,
            consistency_weight=self.weights.consistency,
            mock_weight=self.weights.mock,
            confidence_weight=self.weights.confidence,
        )

    def _total_weight(self) -> int:
        return (
            self.weights.completion
            + self.weights.revision
            + self.weights.consistency
            + self.weights.mock
            + self.weights.confidence
        )
