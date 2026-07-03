"""Topic repository implementations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from mission_control.core.config import ROOT_DIR
from mission_control.study.models import Topic


@dataclass(frozen=True)
class TopicRepository:
    """Load study topics from CSV files."""

    data_dir: Path = ROOT_DIR / "data"

    def load_quant_topics(self) -> list[Topic]:
        """Load Quant topics."""
        return self._load_topics("quant_topics.csv", "Quant")

    def load_dilr_topics(self) -> list[Topic]:
        """Load DILR topics."""
        return self._load_topics("dilr_topics.csv", "DILR")

    def load_varc_topics(self) -> list[Topic]:
        """Load VARC topics."""
        return self._load_topics("verbal_topics.csv", "VARC")

    def load_all_topics(self) -> dict[str, list[Topic]]:
        """Load every subject topic collection."""
        return {
            "Quant": self.load_quant_topics(),
            "DILR": self.load_dilr_topics(),
            "VARC": self.load_varc_topics(),
        }

    def _load_topics(self, filename: str, subject: str) -> list[Topic]:
        path = self.data_dir / filename
        dataframe = pd.read_csv(path)

        if "Topic" not in dataframe.columns:
            raise ValueError(f"Topic CSV missing 'Topic' column: {path}")
        if "Weight" not in dataframe.columns:
            dataframe["Weight"] = 1

        dataframe["Weight"] = dataframe["Weight"].fillna(1).astype(int)
        return [
            Topic(
                name=str(row.Topic),
                weight=max(int(row.Weight), 1),
                subject=subject,
            )
            for row in dataframe.itertuples(index=False)
        ]
