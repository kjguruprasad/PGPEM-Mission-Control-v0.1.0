from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mission_control.application import Application
from mission_control.application.context import ApplicationContext
from mission_control.core.config import WorkbookConfig
from mission_control.revision.services import RevisionService
from mission_control.study.repositories import PlannerRepository, TopicRepository
from mission_control.study.services import PlannerService, StudyService


def test_topic_repository_loads_all_subjects():
    repository = TopicRepository()

    topics = repository.load_all_topics()

    assert set(topics) == {"Quant", "DILR", "VARC"}
    assert topics["Quant"][0].name == "Percentages"
    assert all(topic.weight >= 1 for topic in topics["DILR"])


def test_planner_service_generates_and_persists_plan():
    application = Application()
    repository = PlannerRepository()
    context = application.create_context()
    service = PlannerService(
        planner_generator=_StaticPlanner(context.study_plan),
        planner_repository=repository,
    )

    plan = service.generate_plan()

    assert len(plan) == 106
    assert repository.list() == plan


def test_study_service_creates_subject_tasks():
    context = Application().create_context()

    tasks = StudyService().create_tasks(context.study_plan)

    assert tasks
    assert {task.subject for task in tasks[:3]} == {"Quant", "DILR", "VARC"}


def test_revision_service_creates_revision_schedule():
    context = Application().create_context()

    schedule = RevisionService().create_schedule(context.study_plan)

    assert len(schedule.tasks) == 21
    assert schedule.tasks[0].day == 7


def test_application_calls_renderer(tmp_path):
    renderer = _RecordingRenderer(output_path=tmp_path / "result.xlsx")
    application = Application(
        workbook_config=WorkbookConfig(output_dir=tmp_path),
        renderer=renderer,
    )

    output_path = application.run()

    assert output_path == tmp_path / "result.xlsx"
    assert renderer.context is not None
    assert len(renderer.context.study_plan) == 106
    assert renderer.context.dashboard_data.total_mock_tests == 7


@dataclass
class _StaticPlanner:
    plan: list[object]

    def generate(self) -> list[object]:
        return list(self.plan)


@dataclass
class _RecordingRenderer:
    output_path: Path
    context: ApplicationContext | None = None

    def render(self, context: ApplicationContext) -> Path:
        self.context = context
        return self.output_path
