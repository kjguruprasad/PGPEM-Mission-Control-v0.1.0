"""Command-line entrypoint for workbook generation."""

from __future__ import annotations

from pathlib import Path

from mission_control.core.config import WorkbookConfig
from mission_control.core.logger import get_logger
from mission_control.application import Application


def generate_workbook(config: WorkbookConfig | None = None) -> Path:
    """Generate the PGPEM Mission Control workbook."""
    return Application(workbook_config=config or WorkbookConfig()).run()


def main() -> None:
    """Run the Mission Control application from the command line."""
    logger = get_logger(__name__)
    path = generate_workbook()
    logger.info("Generated workbook: %s", path)


if __name__ == "__main__":
    main()
