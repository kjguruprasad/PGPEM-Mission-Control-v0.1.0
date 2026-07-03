"""Study intelligence report model."""

from __future__ import annotations

from dataclasses import dataclass

from mission_control.analytics.models.learning_velocity import LearningVelocity
from mission_control.analytics.models.readiness_score import ReadinessScore
from mission_control.analytics.models.recommendation import Recommendation
from mission_control.analytics.models.study_statistics import StudyStatistics
from mission_control.analytics.models.weak_topic import WeakTopic


@dataclass(frozen=True)
class StudyDistribution:
    """Prepared study distribution row."""

    subject: str
    task_count: int
    planned_hours: int


@dataclass(frozen=True)
class StudyHoursTrend:
    """Prepared study-hours trend row."""

    day: int
    planned_hours: int
    completed_hours: int


@dataclass(frozen=True)
class StudyIntelligenceReport:
    """Renderer-neutral analytics report."""

    statistics: StudyStatistics
    velocity: LearningVelocity
    weak_topics: tuple[WeakTopic, ...]
    recommendations: tuple[Recommendation, ...]
    readiness: ReadinessScore
    study_distribution: tuple[StudyDistribution, ...]
    study_hours_trend: tuple[StudyHoursTrend, ...]
