"""Core study-domain entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum


class TaskStatus(StrEnum):
    """Study task lifecycle status."""

    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


@dataclass(frozen=True)
class Topic:
    """A study topic."""

    name: str
    weight: int = 1
    subject: str = ""


@dataclass(frozen=True)
class Chapter:
    """A chapter containing topics."""

    title: str
    topics: tuple[Topic, ...] = ()


@dataclass(frozen=True)
class Book:
    """A study resource book."""

    title: str
    author: str = ""
    chapters: tuple[Chapter, ...] = ()


@dataclass(frozen=True)
class StudyTask:
    """A daily study task independent of any renderer."""

    id: str
    day: int
    due_date: date
    subject: str
    topic: str
    planned_hours: int
    status: TaskStatus = TaskStatus.NOT_STARTED
    notes: str = ""


@dataclass(frozen=True)
class StudySession:
    """Actual study time logged by a learner."""

    session_date: date
    subject: str
    duration_hours: float
    topic: str = ""
    notes: str = ""


@dataclass(frozen=True)
class Goal:
    """A measurable learning goal."""

    name: str
    target: str
    due_date: date | None = None
    metric: str = ""
    status: TaskStatus = TaskStatus.NOT_STARTED


@dataclass(frozen=True)
class Habit:
    """A repeatable learning habit."""

    name: str
    frequency: str
    streak: int = 0
    tags: tuple[str, ...] = field(default_factory=tuple)
