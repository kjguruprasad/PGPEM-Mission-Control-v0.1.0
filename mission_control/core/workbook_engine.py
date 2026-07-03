from pathlib import Path

from openpyxl import Workbook

from .constants import OUTPUT_DIR
from .constants import WORKBOOK_NAME

from .logger import get_logger


class WorkbookEngine:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.workbook = Workbook()
        self.logger.info("Workbook initialized")

    def create_sheet(self, name):
        return self.workbook.create_sheet(name)

    def remove_default_sheet(self):
        sheet = self.workbook.active
        self.workbook.remove(sheet)

    def save(self):
        OUTPUT_DIR.mkdir(exist_ok=True)
        path = OUTPUT_DIR / WORKBOOK_NAME
        self.workbook.save(path)
        self.logger.info(f"Workbook saved to {path}")
        return path