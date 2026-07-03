"""Recommendation service."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from mission_control.analytics.models import (
    Recommendation,
    StudyStatistics,
    WeakTopic,
)
from mission_control.revision.models import RevisionSchedule


@dataclass(frozen=True)
class RecommendationService:
    """Generate actionable recommendations from analytics outputs."""

    def generate(
        self,
        *,
        statistics: StudyStatistics,
        revision_schedule: RevisionSchedule,
        weak_topics: tuple[WeakTopic, ...],
        generated_date: date | None = None,
    ) -> tuple[Recommendation, ...]:
        """Return prioritized recommendations."""
        effective_date = generated_date or date.today()
        recommendations: list[Recommendation] = []

        if weak_topics:
            weakest = weak_topics[0]
            recommendations.append(
                Recommendation(
                    title=f"{weakest.topic} accuracy is below 60%.",
                    description=f"Study {weakest.topic} tomorrow.",
                    priority="High",
                    category="Weak Topic",
                    generated_date=effective_date,
                )
            )

        if revision_schedule.overdue:
            recommendations.append(
                Recommendation(
                    title=f"You have {revision_schedule.overdue} overdue revisions.",
                    description="Clear overdue revisions before adding new topics.",
                    priority="Medium",
                    category="Revision",
                    generated_date=effective_date,
                )
            )

        if statistics.pending_tasks:
            recommendations.append(
                Recommendation(
                    title=f"{statistics.pending_tasks} study tasks are pending.",
                    description="Prioritize the next pending task today.",
                    priority="Low",
                    category="Study Plan",
                    generated_date=effective_date,
                )
            )

        return tuple(recommendations)
