"""Command-line entrypoint for workbook generation."""

from __future__ import annotations

from pathlib import Path

from mission_control.core.config import WorkbookConfig
from mission_control.core.logger import get_logger
from mission_control.workbook.builder import WorkbookBuilder


def generate_workbook(config: WorkbookConfig | None = None) -> Path:
    """Generate the PGPEM Mission Control workbook."""
    return (
        WorkbookBuilder(config=config)
        .add_dashboard()
        .add_goal_sheet()
        .add_planner()
        .add_daily_planner()
        .add_quant_tracker()
        .add_dilr_tracker()
        .add_varc_tracker()
        .add_vocabulary()
        .add_revision_tracker()
        .add_mock_tests()
        .add_analytics()
        .add_habits()
        .add_notes()
        .add_interview_prep()
        .add_settings()
        .build()
    )


def main() -> None:
    """Run workbook generation from the command line."""
    logger = get_logger(__name__)
    path = generate_workbook()
    logger.info("Generated workbook: %s", path)


if __name__ == "__main__":
    main()
