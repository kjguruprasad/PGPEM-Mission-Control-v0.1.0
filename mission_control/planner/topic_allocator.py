"""Weighted topic allocation for planner rows."""

from __future__ import annotations

from itertools import cycle
from pathlib import Path

import pandas as pd

from mission_control.planner.models import Topic


class TopicAllocator:
    """Allocate Quant, DILR, and VARC topics from weighted CSV files."""

    def __init__(
        self,
        *,
        quant_topics: list[Topic],
        dilr_topics: list[Topic],
        verbal_topics: list[Topic],
    ) -> None:
        self._quant_cycle = cycle(self._weighted_names(quant_topics))
        self._dilr_cycle = cycle(self._weighted_names(dilr_topics))
        self._verbal_cycle = cycle(self._weighted_names(verbal_topics))

    @classmethod
    def from_csv_files(
        cls,
        *,
        quant_path: Path,
        dilr_path: Path,
        verbal_path: Path,
    ) -> "TopicAllocator":
        """Create an allocator from configured CSV files."""
        return cls(
            quant_topics=cls._read_topics(quant_path),
            dilr_topics=cls._read_topics(dilr_path),
            verbal_topics=cls._read_topics(verbal_path),
        )

    def next_quant_topic(self) -> str:
        """Return the next Quant topic."""
        return next(self._quant_cycle)

    def next_dilr_topic(self) -> str:
        """Return the next DILR topic."""
        return next(self._dilr_cycle)

    def next_varc_topic(self) -> str:
        """Return the next VARC topic."""
        return next(self._verbal_cycle)

    @staticmethod
    def _read_topics(path: Path) -> list[Topic]:
        dataframe = pd.read_csv(path)
        if "Topic" not in dataframe.columns:
            raise ValueError(f"Topic CSV missing 'Topic' column: {path}")

        if "Weight" not in dataframe.columns:
            dataframe["Weight"] = 1

        dataframe["Weight"] = dataframe["Weight"].fillna(1).astype(int)

        return [
            Topic(name=str(row.Topic), weight=max(int(row.Weight), 1))
            for row in dataframe.itertuples(index=False)
        ]

    @staticmethod
    def _weighted_names(topics: list[Topic]) -> list[str]:
        if not topics:
            raise ValueError("At least one topic is required for allocation.")

        weighted_names: list[str] = []
        for topic in topics:
            weighted_names.extend([topic.name] * topic.weight)
        return weighted_names
