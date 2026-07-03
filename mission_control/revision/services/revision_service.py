"""Revision scheduling service."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from mission_control.common.logging import get_logger
from mission_control.core.config import AppConfig, load_app_config
from mission_control.revision.models import (
    RevisionSchedule,
    RevisionStatus,
    RevisionTask,
)
from mission_control.study.models import StudyTask, TaskStatus


@dataclass(frozen=True)
class RevisionService:
    """Generate and evaluate spaced-repetition revision tasks."""

    app_config: AppConfig | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "logger", get_logger(__name__))

    @property
    def intervals(self) -> tuple[int, ...]:
        """Return configured spaced-repetition intervals in days."""
        config = self.app_config or load_app_config()
        return config.revision.intervals

    def create_schedule(
        self,
        study_tasks: list[StudyTask],
        *,
        today: date | None = None,
    ) -> RevisionSchedule:
        """Generate a typed revision schedule from completed study tasks."""
        revision_tasks = self.generate_revision_tasks(
            study_tasks,
            today=today,
        )
        return self.summarize(revision_tasks, today=today)

    def generate_revision_tasks(
        self,
        study_tasks: list[StudyTask],
        *,
        today: date | None = None,
    ) -> tuple[RevisionTask, ...]:
        """Generate spaced-repetition tasks for completed study tasks."""
        effective_today = today or date.today()
        revision_tasks: list[RevisionTask] = []

        for study_task in study_tasks:
            if study_task.status != TaskStatus.COMPLETED:
                continue

            for revision_number, interval_days in enumerate(self.intervals, start=1):
                scheduled_date = study_task.due_date + timedelta(days=interval_days)
                status = self._status_for(
                    scheduled_date=scheduled_date,
                    completed=False,
                    today=effective_today,
                )
                revision_tasks.append(
                    RevisionTask(
                        id=f"{study_task.id}-r{revision_number}",
                        study_task_id=study_task.id,
                        topic=study_task.topic,
                        revision_number=revision_number,
                        scheduled_date=scheduled_date,
                        status=status,
                    )
                )

        self.logger.info("Generated %s revision tasks", len(revision_tasks))
        return tuple(revision_tasks)

    def due_today(
        self,
        revision_tasks: tuple[RevisionTask, ...],
        *,
        today: date | None = None,
    ) -> tuple[RevisionTask, ...]:
        """Return revisions scheduled for today."""
        effective_today = today or date.today()
        return tuple(
            task
            for task in revision_tasks
            if task.scheduled_date == effective_today
            and task.status != RevisionStatus.COMPLETED
        )

    def overdue(
        self,
        revision_tasks: tuple[RevisionTask, ...],
        *,
        today: date | None = None,
    ) -> tuple[RevisionTask, ...]:
        """Return overdue revisions."""
        effective_today = today or date.today()
        return tuple(
            task
            for task in revision_tasks
            if task.scheduled_date < effective_today
            and task.status != RevisionStatus.COMPLETED
        )

    def completion_percentage(
        self,
        revision_tasks: tuple[RevisionTask, ...],
    ) -> int:
        """Return completion percentage for revision tasks."""
        if not revision_tasks:
            return 0
        completed = sum(1 for task in revision_tasks if task.completed)
        return round((completed / len(revision_tasks)) * 100)

    def summarize(
        self,
        revision_tasks: tuple[RevisionTask, ...],
        *,
        today: date | None = None,
    ) -> RevisionSchedule:
        """Return aggregate revision schedule metrics."""
        effective_today = today or date.today()
        completed = sum(1 for task in revision_tasks if task.completed)
        overdue = len(self.overdue(revision_tasks, today=effective_today))

        return RevisionSchedule(
            revision_tasks=revision_tasks,
            total_due=len(revision_tasks),
            completed=completed,
            overdue=overdue,
        )

    @staticmethod
    def _status_for(
        *,
        scheduled_date: date,
        completed: bool,
        today: date,
    ) -> RevisionStatus:
        if completed:
            return RevisionStatus.COMPLETED
        if scheduled_date < today:
            return RevisionStatus.OVERDUE
        return RevisionStatus.PENDING
