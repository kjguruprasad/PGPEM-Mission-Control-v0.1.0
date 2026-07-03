"""Study analytics service."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date

from mission_control.analytics.models import (
    StudyDistribution,
    StudyHoursTrend,
    StudyStatistics,
    WeakTopic,
)
from mission_control.revision.models import RevisionSchedule
from mission_control.study.models import StudyTask, TaskStatus


@dataclass(frozen=True)
class AnalyticsService:
    """Calculate study statistics from renderer-neutral data."""

    weak_topic_threshold: int = 70

    def calculate_statistics(
        self,
        study_tasks: list[StudyTask],
        revision_schedule: RevisionSchedule,
        *,
        today: date | None = None,
    ) -> StudyStatistics:
        """Return aggregate study statistics."""
        effective_today = today or date.today()
        total_tasks = len(study_tasks)
        completed_tasks = sum(
            1 for task in study_tasks if task.status == TaskStatus.COMPLETED
        )
        pending_tasks = total_tasks - completed_tasks
        overdue_tasks = sum(
            1
            for task in study_tasks
            if task.status != TaskStatus.COMPLETED
            and task.due_date < effective_today
        )
        total_hours = sum(task.planned_hours for task in study_tasks)
        completed_hours = sum(
            task.planned_hours
            for task in study_tasks
            if task.status == TaskStatus.COMPLETED
        )
        completion = round((completed_tasks / total_tasks) * 100) if total_tasks else 0

        return StudyStatistics(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            pending_tasks=pending_tasks,
            overdue_tasks=overdue_tasks,
            total_hours=total_hours,
            completed_hours=completed_hours,
            completion_percentage=completion,
            revision_completion_percentage=self._revision_completion(
                revision_schedule,
            ),
        )

    def identify_weak_topics(
        self,
        study_tasks: list[StudyTask],
    ) -> tuple[WeakTopic, ...]:
        """Infer weak topics from pending workload until performance data exists."""
        attempts_by_topic: dict[str, int] = defaultdict(int)
        pending_by_topic: dict[str, int] = defaultdict(int)

        for task in study_tasks:
            attempts_by_topic[task.topic] += 1
            if task.status != TaskStatus.COMPLETED:
                pending_by_topic[task.topic] += 1

        weak_topics: list[WeakTopic] = []
        for topic, attempts in attempts_by_topic.items():
            pending = pending_by_topic[topic]
            accuracy = round(((attempts - pending) / attempts) * 100)
            if accuracy >= self.weak_topic_threshold:
                continue
            priority = "High" if accuracy < 60 else "Medium"
            weak_topics.append(
                WeakTopic(
                    topic=topic,
                    attempts=attempts,
                    accuracy=accuracy,
                    confidence=max(accuracy, 10),
                    priority=priority,
                )
            )

        return tuple(sorted(weak_topics, key=lambda item: item.accuracy)[:10])

    def study_distribution(
        self,
        study_tasks: list[StudyTask],
    ) -> tuple[StudyDistribution, ...]:
        """Return prepared subject distribution rows."""
        counts: dict[str, int] = defaultdict(int)
        hours: dict[str, int] = defaultdict(int)

        for task in study_tasks:
            counts[task.subject] += 1
            hours[task.subject] += task.planned_hours

        return tuple(
            StudyDistribution(
                subject=subject,
                task_count=counts[subject],
                planned_hours=hours[subject],
            )
            for subject in sorted(counts)
        )

    def study_hours_trend(
        self,
        study_tasks: list[StudyTask],
    ) -> tuple[StudyHoursTrend, ...]:
        """Return prepared daily hours trend rows."""
        planned: dict[int, int] = defaultdict(int)
        completed: dict[int, int] = defaultdict(int)

        for task in study_tasks:
            planned[task.day] += task.planned_hours
            if task.status == TaskStatus.COMPLETED:
                completed[task.day] += task.planned_hours

        return tuple(
            StudyHoursTrend(
                day=day,
                planned_hours=planned[day],
                completed_hours=completed[day],
            )
            for day in sorted(planned)
        )

    @staticmethod
    def _revision_completion(revision_schedule: RevisionSchedule) -> int:
        if revision_schedule.total_due == 0:
            return 0
        return round(
            (revision_schedule.completed / revision_schedule.total_due) * 100,
        )
