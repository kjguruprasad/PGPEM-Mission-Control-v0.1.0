"""Date utilities."""

from __future__ import annotations

from datetime import date


def is_weekend(value: date) -> bool:
    """Return whether a date falls on Saturday or Sunday."""
    return value.weekday() >= 5
