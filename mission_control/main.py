from mission_control.core.workbook_engine import WorkbookEngine


def main():
    engine = WorkbookEngine()
    engine.remove_default_sheet()
    dashboard = engine.create_sheet("Dashboard")
    dashboard["A1"] = "PGPEM Mission Control"
    dashboard["A2"] = "Workbook Generator v0.1.0"
    engine.save()


if __name__ == "__main__":
    main()