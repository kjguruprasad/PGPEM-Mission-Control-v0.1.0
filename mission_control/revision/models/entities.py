"""Revision-domain entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RevisionTask:
    """A scheduled revision task."""

    day: int
    revision_date: date
    label: str
    notes: str = ""


@dataclass(frozen=True)
class RevisionSchedule:
    """A collection of revision tasks."""

    tasks: tuple[RevisionTask, ...]
