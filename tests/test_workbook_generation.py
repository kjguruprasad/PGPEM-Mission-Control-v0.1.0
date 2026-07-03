from __future__ import annotations

from openpyxl import load_workbook

from mission_control.core.config import WorkbookConfig
from mission_control.main import generate_workbook


EXPECTED_SHEETS = [
    "Dashboard",
    "SMART Goals",
    "106-Day Planner",
    "Daily Planner",
    "Quant Tracker",
    "DILR Tracker",
    "VARC Tracker",
    "Vocabulary",
    "Revision Tracker",
    "Mock Tests",
    "Analytics",
    "Habits",
    "Notes",
    "Interview Prep",
    "Settings",
]


def test_generate_workbook_creates_all_registered_sheets(tmp_path):
    config = WorkbookConfig(output_dir=tmp_path)

    workbook_path = generate_workbook(config)

    assert workbook_path == tmp_path / "PGPEM_Mission_Control.xlsx"
    assert workbook_path.exists()

    workbook = load_workbook(workbook_path)
    assert workbook.sheetnames == EXPECTED_SHEETS

    dashboard = workbook["Dashboard"]
    assert dashboard["A1"].value == "PGPEM Mission Control"
    assert dashboard["A4"].value == "Readiness Score"
    assert dashboard["A8"].value == "Track"
    assert dashboard["A9"].value == "Quantitative Aptitude"
    assert len(dashboard._charts) == 1


def test_dashboard_has_expected_formatting(tmp_path):
    workbook_path = generate_workbook(WorkbookConfig(output_dir=tmp_path))
    dashboard = load_workbook(workbook_path)["Dashboard"]

    assert dashboard.sheet_view.showGridLines is False
    assert dashboard.freeze_panes == "A9"
    assert dashboard["A8"].fill.fgColor.rgb == "001F4E78"
    assert dashboard.column_dimensions["A"].width >= 20


def test_standard_sheets_have_titles_headers_and_frozen_header_rows(tmp_path):
    workbook_path = generate_workbook(WorkbookConfig(output_dir=tmp_path))
    workbook = load_workbook(workbook_path)

    for sheet_name in EXPECTED_SHEETS[1:]:
        worksheet = workbook[sheet_name]
        assert worksheet["A1"].value == sheet_name
        assert worksheet["A4"].value is not None
        assert worksheet.freeze_panes == "A5"
        assert worksheet.sheet_view.showGridLines is False


def test_yaml_config_drives_planner_and_settings(tmp_path):
    workbook_path = generate_workbook(WorkbookConfig(output_dir=tmp_path))
    workbook = load_workbook(workbook_path)

    planner = workbook["106-Day Planner"]
    settings = workbook["Settings"]

    assert planner["A7"].value == 106
    assert settings["B7"].value == 106
