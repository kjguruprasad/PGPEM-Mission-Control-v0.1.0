"""Application orchestration for PGPEM Mission Control."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from mission_control.application.context import ApplicationContext
from mission_control.common.config import ConfigurationRepository
from mission_control.common.logging import get_logger
from mission_control.core.config import WorkbookConfig
from mission_control.dashboard.services import DashboardService
from mission_control.mocks.services import MockService
from mission_control.planner.planner_generator import PlannerGenerator
from mission_control.renderers import Renderer
from mission_control.renderers.excel import ExcelRenderer
from mission_control.revision.services import RevisionService
from mission_control.study.repositories import PlannerRepository, TopicRepository
from mission_control.study.services import (
    PlannerService,
    ProgressService,
    StudyService,
)


@dataclass
class Application:
    """Top-level application composition root."""

    workbook_config: WorkbookConfig = field(default_factory=WorkbookConfig)
    configuration_repository: ConfigurationRepository = field(
        default_factory=ConfigurationRepository,
    )
    topic_repository: TopicRepository = field(default_factory=TopicRepository)
    planner_repository: PlannerRepository = field(
        default_factory=PlannerRepository,
    )
    renderer: Renderer | None = None

    def __post_init__(self) -> None:
        self.logger = get_logger(__name__)

    def run(self) -> Path:
        """Execute the learning operating system workflow."""
        context = self.create_context()
        renderer = self.renderer or ExcelRenderer(self.workbook_config)
        output_path = renderer.render(context)
        self.logger.info("Application rendered output to %s", output_path)
        return output_path

    def create_context(self) -> ApplicationContext:
        """Load inputs, execute services, and return renderer-neutral data."""
        app_config = self.workbook_config.app
        self.topic_repository.load_all_topics()

        planner_generator = PlannerGenerator.from_app_config(
            app_config=app_config,
        )
        planner_service = PlannerService(
            planner_generator=planner_generator,
            planner_repository=self.planner_repository,
        )
        study_service = StudyService()
        progress_service = ProgressService()
        revision_service = RevisionService(app_config=app_config)
        mock_service = MockService()
        dashboard_service = DashboardService()

        study_plan = planner_service.generate_plan()
        study_tasks = study_service.create_tasks(study_plan)
        progress = progress_service.calculate(study_plan)
        revision_schedule = revision_service.create_schedule(study_tasks)
        mock_tests = mock_service.create_mock_tests(study_plan)
        dashboard_data = dashboard_service.build(
            progress=progress,
            revision_schedule=revision_schedule,
            mock_tests=mock_tests,
        )

        return ApplicationContext(
            app_config=app_config,
            study_plan=study_plan,
            study_tasks=study_tasks,
            revision_schedule=revision_schedule,
            mock_tests=mock_tests,
            dashboard_data=dashboard_data,
        )
