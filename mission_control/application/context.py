"""Application execution context."""

from __future__ import annotations

from dataclasses import dataclass

from mission_control.analytics.models import StudyIntelligenceReport
from mission_control.core.config import AppConfig
from mission_control.dashboard.services import DashboardData
from mission_control.mocks.models import MockTest
from mission_control.planner.models import StudyPlanDay
from mission_control.revision.models import RevisionSchedule
from mission_control.study.models import StudyTask


@dataclass(frozen=True)
class ApplicationContext:
    """Renderer-neutral output of application business logic."""

    app_config: AppConfig
    study_plan: list[StudyPlanDay]
    study_tasks: list[StudyTask]
    revision_schedule: RevisionSchedule
    mock_tests: list[MockTest]
    dashboard_data: DashboardData
    study_intelligence: StudyIntelligenceReport
