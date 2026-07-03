"""Weak-topic model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeakTopic:
    """Topic needing attention."""

    topic: str
    attempts: int
    accuracy: int
    confidence: int
    priority: str
