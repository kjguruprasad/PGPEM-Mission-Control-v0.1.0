"""Workbook theme tokens."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    """Centralized style values used across workbook sheets."""

    primary: str = "1F4E78"
    primary_dark: str = "17365D"
    secondary: str = "D9EAD3"
    accent: str = "9FC5E8"
    success: str = "6AA84F"
    warning: str = "F1C232"
    danger: str = "CC0000"
    neutral: str = "F3F6FA"
    white: str = "FFFFFF"
    border: str = "D9E2F3"
    text: str = "1F2937"
    muted_text: str = "6B7280"
    header_font: str = "Calibri"
    body_font: str = "Calibri"
    title_size: int = 18
    subtitle_size: int = 11
    header_size: int = 12
    body_size: int = 11
