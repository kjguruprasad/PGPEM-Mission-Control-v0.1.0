"""Study task service."""

from __future__ import annotations

from dataclasses import dataclass

from mission_control.planner.models import StudyPlanDay
from mission_control.study.models import StudyTask


@dataclass(frozen=True)
class StudyService:
    """Create renderer-neutral study tasks from a generated plan."""

    def create_tasks(self, plan: list[StudyPlanDay]) -> list[StudyTask]:
        """Create one task per subject topic on active study days."""
        tasks: list[StudyTask] = []

        for plan_day in plan:
            topics = {
                "Quant": plan_day.quant_topic,
                "DILR": plan_day.dilr_topic,
                "VARC": plan_day.varc_topic,
            }
            active_topics = {
                subject: topic
                for subject, topic in topics.items()
                if topic
            }
            if not active_topics:
                continue

            planned_hours = max(plan_day.study_hours // len(active_topics), 1)
            for subject, topic in active_topics.items():
                tasks.append(
                    StudyTask(
                        id=f"study-{plan_day.day:03d}-{subject.lower()}",
                        day=plan_day.day,
                        due_date=plan_day.date,
                        subject=subject,
                        topic=topic,
                        planned_hours=planned_hours,
                        status=plan_day.status,
                        notes=plan_day.notes,
                    )
                )

        return tasks
