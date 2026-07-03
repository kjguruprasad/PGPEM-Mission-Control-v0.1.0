"""Revision-domain entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class RevisionStatus(StrEnum):
    """Revision task lifecycle status."""

    PENDING = "Pending"
    COMPLETED = "Completed"
    OVERDUE = "Overdue"


@dataclass(frozen=True)
class RevisionTask:
    """A spaced-repetition task for a completed study task."""

    id: str
    study_task_id: str
    topic: str
    revision_number: int
    scheduled_date: date
    completed: bool = False
    completed_date: date | None = None
    status: RevisionStatus = RevisionStatus.PENDING
    notes: str = ""


@dataclass(frozen=True)
class RevisionSchedule:
    """A typed collection of revision tasks and aggregate counts."""

    revision_tasks: tuple[RevisionTask, ...]
    total_due: int
    completed: int
    overdue: int

    @property
    def tasks(self) -> tuple[RevisionTask, ...]:
        """Backward-compatible alias for callers using the old model."""
        return self.revision_tasks
