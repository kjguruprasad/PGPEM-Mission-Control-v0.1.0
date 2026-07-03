from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    PRIMARY = "1F4E78"
    SECONDARY = "D9EAD3"
    SUCCESS = "6AA84F"
    WARNING = "F1C232"
    DANGER = "CC0000"
    HEADER_FONT = "Calibri"
    BODY_FONT = "Calibri"
    TITLE_SIZE = 18
    HEADER_SIZE = 12
    BODY_SIZE = 11