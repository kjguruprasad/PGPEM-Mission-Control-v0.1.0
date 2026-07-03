from __future__ import annotations

from datetime import date

from openpyxl import load_workbook

from mission_control.core.config import WorkbookConfig
from mission_control.main import generate_workbook
from mission_control.revision.models import RevisionStatus, RevisionTask
from mission_control.revision.services import RevisionService
from mission_control.study.models import StudyTask, TaskStatus


def test_revision_generation_creates_tasks_for_completed_study_tasks():
    service = RevisionService()
    study_task = _study_task()

    revision_tasks = service.generate_revision_tasks(
        [study_task],
        today=date(2026, 7, 1),
    )

    assert len(revision_tasks) == 5
    assert revision_tasks[0].study_task_id == "study-001-quant"
    assert revision_tasks[0].topic == "Percentages"


def test_revision_interval_calculations_follow_settings():
    service = RevisionService()
    study_task = _study_task(due_date=date(2026, 7, 10))

    revision_tasks = service.generate_revision_tasks(
        [study_task],
        today=date(2026, 7, 10),
    )

    assert [task.scheduled_date for task in revision_tasks] == [
        date(2026, 7, 11),
        date(2026, 7, 13),
        date(2026, 7, 17),
        date(2026, 7, 24),
        date(2026, 8, 9),
    ]


def test_revision_overdue_detection():
    service = RevisionService()
    revision_tasks = (
        RevisionTask(
            id="r1",
            study_task_id="s1",
            topic="Algebra",
            revision_number=1,
            scheduled_date=date(2026, 7, 1),
            status=RevisionStatus.OVERDUE,
        ),
        RevisionTask(
            id="r2",
            study_task_id="s1",
            topic="Algebra",
            revision_number=2,
            scheduled_date=date(2026, 7, 5),
        ),
    )

    overdue = service.overdue(revision_tasks, today=date(2026, 7, 3))

    assert [task.id for task in overdue] == ["r1"]


def test_revision_completion_percentage():
    service = RevisionService()
    revision_tasks = (
        RevisionTask(
            id="r1",
            study_task_id="s1",
            topic="Algebra",
            revision_number=1,
            scheduled_date=date(2026, 7, 1),
            completed=True,
            completed_date=date(2026, 7, 1),
            status=RevisionStatus.COMPLETED,
        ),
        RevisionTask(
            id="r2",
            study_task_id="s1",
            topic="Algebra",
            revision_number=2,
            scheduled_date=date(2026, 7, 3),
        ),
    )

    assert service.completion_percentage(revision_tasks) == 50


def test_revision_planner_workbook_sheet_generated(tmp_path):
    workbook_path = generate_workbook(WorkbookConfig(output_dir=tmp_path))

    workbook = load_workbook(workbook_path)
    worksheet = workbook["Revision Planner"]

    assert worksheet["A1"].value == "Revision Planner"
    assert worksheet["A4"].value == "Revision ID"
    assert worksheet.auto_filter.ref == "A4:I4"
    assert worksheet.freeze_panes == "A5"


def _study_task(
    *,
    due_date: date = date(2026, 7, 10),
    status: TaskStatus = TaskStatus.COMPLETED,
) -> StudyTask:
    return StudyTask(
        id="study-001-quant",
        day=1,
        due_date=due_date,
        subject="Quant",
        topic="Percentages",
        planned_hours=1,
        status=status,
    )
