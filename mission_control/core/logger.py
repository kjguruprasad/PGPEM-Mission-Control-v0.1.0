"""Logging helpers for PGPEM Mission Control."""

from __future__ import annotations

import logging
import sys


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    """Configure application logging once for console execution."""
    root_logger = logging.getLogger("mission_control")
    root_logger.setLevel(level)
    root_logger.propagate = False

    if root_logger.handlers:
        for handler in root_logger.handlers:
            handler.setLevel(level)
        return

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Return a module logger under the package logging namespace."""
    configure_logging()
    return logging.getLogger(name)
