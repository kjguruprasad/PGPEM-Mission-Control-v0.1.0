from __future__ import annotations

from datetime import date

from openpyxl import load_workbook

from mission_control.analytics.services import (
    AnalyticsService,
    ReadinessService,
    RecommendationService,
    VelocityService,
)
from mission_control.core.config import ReadinessWeightsConfig, WorkbookConfig
from mission_control.main import generate_workbook
from mission_control.revision.models import RevisionSchedule, RevisionStatus
from mission_control.revision.models import RevisionTask
from mission_control.study.models import StudyTask, TaskStatus


def test_analytics_service_calculates_study_statistics():
    service = AnalyticsService()
    statistics = service.calculate_statistics(
        _study_tasks(),
        _revision_schedule(),
        today=date(2026, 7, 5),
    )

    assert statistics.total_tasks == 2
    assert statistics.completed_tasks == 1
    assert statistics.pending_tasks == 1
    assert statistics.overdue_tasks == 1
    assert statistics.total_hours == 5
    assert statistics.completed_hours == 2
    assert statistics.completion_percentage == 50
    assert statistics.revision_completion_percentage == 50


def test_velocity_service_calculates_learning_velocity():
    statistics = AnalyticsService().calculate_statistics(
        _study_tasks(),
        _revision_schedule(),
        today=date(2026, 7, 5),
    )

    velocity = VelocityService().calculate(
        statistics,
        elapsed_days=2,
        total_questions=20,
    )

    assert velocity.study_hours_per_day == 1
    assert velocity.questions_per_day == 10
    assert velocity.questions_per_hour == 10
    assert velocity.average_completion_rate == 0.5
    assert velocity.projected_completion_date is not None


def test_readiness_service_uses_weighted_score():
    statistics = AnalyticsService().calculate_statistics(
        _study_tasks(),
        _revision_schedule(),
        today=date(2026, 7, 5),
    )
    service = ReadinessService(weights=ReadinessWeightsConfig())

    readiness = service.calculate(
        statistics,
        consistency_score=50,
        mock_score=50,
        confidence_score=50,
    )

    assert readiness.score == 50
    assert readiness.completion_weight == 30


def test_recommendation_service_generates_prioritized_actions():
    analytics = AnalyticsService(weak_topic_threshold=70)
    statistics = analytics.calculate_statistics(
        _study_tasks(),
        _revision_schedule(),
        today=date(2026, 7, 5),
    )
    weak_topics = analytics.identify_weak_topics(_study_tasks())

    recommendations = RecommendationService().generate(
        statistics=statistics,
        revision_schedule=_revision_schedule(),
        weak_topics=weak_topics,
        generated_date=date(2026, 7, 5),
    )

    assert recommendations
    assert recommendations[0].priority == "High"
    assert "Algebra" in recommendations[0].title


def test_study_intelligence_workbook_sheet_generated(tmp_path):
    workbook_path = generate_workbook(WorkbookConfig(output_dir=tmp_path))

    workbook = load_workbook(workbook_path)
    worksheet = workbook["Study Intelligence"]

    assert worksheet["A1"].value == "Study Intelligence"
    assert worksheet["A4"].value == "Overall Statistics"
    assert worksheet["A5"].value == "Metric"
    assert len(worksheet._charts) == 3


def _study_tasks() -> list[StudyTask]:
    return [
        StudyTask(
            id="study-001-quant",
            day=1,
            due_date=date(2026, 7, 1),
            subject="Quant",
            topic="Algebra",
            planned_hours=2,
            status=TaskStatus.COMPLETED,
        ),
        StudyTask(
            id="study-002-quant",
            day=2,
            due_date=date(2026, 7, 2),
            subject="Quant",
            topic="Algebra",
            planned_hours=3,
            status=TaskStatus.NOT_STARTED,
        ),
    ]


def _revision_schedule() -> RevisionSchedule:
    tasks = (
        RevisionTask(
            id="r1",
            study_task_id="study-001-quant",
            topic="Algebra",
            revision_number=1,
            scheduled_date=date(2026, 7, 2),
            completed=True,
            completed_date=date(2026, 7, 2),
            status=RevisionStatus.COMPLETED,
        ),
        RevisionTask(
            id="r2",
            study_task_id="study-001-quant",
            topic="Algebra",
            revision_number=2,
            scheduled_date=date(2026, 7, 4),
            status=RevisionStatus.OVERDUE,
        ),
    )
    return RevisionSchedule(
        revision_tasks=tasks,
        total_due=2,
        completed=1,
        overdue=1,
    )
