"""Automatic 106-day study planner generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mission_control.core.config import (
    DEFAULT_SETTINGS_PATH,
    ROOT_DIR,
    AppConfig,
    load_app_config,
)
from mission_control.core.logger import get_logger
from mission_control.planner.calendar import CalendarGenerator
from mission_control.planner.models import StudyPlanDay
from mission_control.planner.scheduler import Scheduler
from mission_control.planner.topic_allocator import TopicAllocator


@dataclass(frozen=True)
class PlannerDataPaths:
    """Input data locations for planner generation."""

    quant_topics: Path = ROOT_DIR / "data" / "quant_topics.csv"
    dilr_topics: Path = ROOT_DIR / "data" / "dilr_topics.csv"
    verbal_topics: Path = ROOT_DIR / "data" / "verbal_topics.csv"


class PlannerGenerator:
    """Generate a complete 106-day study plan from config and topic data."""

    def __init__(
        self,
        *,
        app_config: AppConfig,
        calendar_generator: CalendarGenerator,
        scheduler: Scheduler,
        topic_allocator: TopicAllocator,
    ) -> None:
        self.app_config = app_config
        self.calendar_generator = calendar_generator
        self.scheduler = scheduler
        self.topic_allocator = topic_allocator
        self.logger = get_logger(__name__)
        self._plan_cache: list[StudyPlanDay] | None = None

    @classmethod
    def from_files(
        cls,
        *,
        settings_path: Path = DEFAULT_SETTINGS_PATH,
        data_paths: PlannerDataPaths | None = None,
    ) -> "PlannerGenerator":
        """Build a planner generator from YAML and CSV files."""
        app_config = load_app_config(settings_path)
        paths = data_paths or PlannerDataPaths()
        return cls.from_app_config(app_config=app_config, data_paths=paths)

    @classmethod
    def from_app_config(
        cls,
        *,
        app_config: AppConfig,
        data_paths: PlannerDataPaths | None = None,
    ) -> "PlannerGenerator":
        """Build a planner generator from injected app config."""
        paths = data_paths or PlannerDataPaths()
        return cls(
            app_config=app_config,
            calendar_generator=CalendarGenerator(
                exam_date=app_config.exam.exam_date,
                duration_days=app_config.planner.duration_days,
            ),
            scheduler=Scheduler(app_config),
            topic_allocator=TopicAllocator.from_csv_files(
                quant_path=paths.quant_topics,
                dilr_path=paths.dilr_topics,
                verbal_path=paths.verbal_topics,
            ),
        )

    def generate(self) -> list[StudyPlanDay]:
        """Generate all planner rows."""
        if self._plan_cache is not None:
            return list(self._plan_cache)

        plan: list[StudyPlanDay] = []

        for calendar_day in self.calendar_generator.generate():
            schedule = self.scheduler.schedule(calendar_day)
            if schedule.revision_only:
                quant_topic = ""
                dilr_topic = ""
                varc_topic = ""
            else:
                quant_topic = self.topic_allocator.next_quant_topic()
                dilr_topic = self.topic_allocator.next_dilr_topic()
                varc_topic = self.topic_allocator.next_varc_topic()

            plan.append(
                StudyPlanDay(
                    day=calendar_day.day,
                    date=calendar_day.date,
                    week=calendar_day.week,
                    day_of_week=calendar_day.day_of_week,
                    quant_topic=quant_topic,
                    dilr_topic=dilr_topic,
                    varc_topic=varc_topic,
                    revision=schedule.revision,
                    mock_test=schedule.mock_test,
                    study_hours=schedule.study_hours,
                )
            )

        self.logger.info("Generated %s planner rows", len(plan))
        self._plan_cache = plan
        return list(plan)
