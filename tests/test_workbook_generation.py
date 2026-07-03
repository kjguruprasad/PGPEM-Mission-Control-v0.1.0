from __future__ import annotations

from openpyxl import load_workbook

from mission_control.core.config import WorkbookConfig
from mission_control.main import generate_workbook


def test_generate_workbook_creates_dashboard(tmp_path):
    config = WorkbookConfig(output_dir=tmp_path)

    workbook_path = generate_workbook(config)

    assert workbook_path == tmp_path / "PGPEM_Mission_Control.xlsx"
    assert workbook_path.exists()

    workbook = load_workbook(workbook_path)
    assert workbook.sheetnames == ["Dashboard"]

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
    assert dashboard.freeze_panes == "A8"
    assert dashboard["A8"].fill.fgColor.rgb == "001F4E78"
    assert dashboard.column_dimensions["A"].width == 20
