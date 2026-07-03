"""Concrete workbook sheet definitions."""

from __future__ import annotations

from mission_control.workbook.table_sheet import TableSheet


class SmartGoalsSheet(TableSheet):
    title = "SMART Goals"
    headers = ["Goal", "Specific Outcome", "Metric", "Target Date", "Status"]
    sample_rows = [
        ("Quant accuracy", "Improve arithmetic accuracy", "85%", "Day 45", "Planned"),
        ("Mock readiness", "Complete full mock review loop", "10 mocks", "Day 90", "Planned"),
    ]


class Planner106DaySheet(TableSheet):
    title = "106-Day Planner"
    headers = ["Day", "Date", "Primary Focus", "Task", "Target", "Done"]

    @property
    def sample_rows(self) -> list[tuple[int, str, str, str, str, str]]:
        days = self.app_config.exam.days
        return [
            (1, "", "Diagnostic", "Baseline mock and review", "1 mock", "No"),
            (days // 2, "", "Checkpoint", "Mid-plan progress audit", "1 review", "No"),
            (days, "", "Final Review", "Formula and strategy revision", "2 hours", "No"),
        ]


class DailyPlannerSheet(TableSheet):
    title = "Daily Planner"
    headers = ["Date", "Available Time", "Priority 1", "Priority 2", "Review", "Energy"]
    sample_rows = [
        ("", "90 min", "Quant drills", "Vocabulary", "Error log", "Medium"),
        ("", "60 min", "VARC passage", "Formula revision", "Notes", "High"),
    ]


class QuantTrackerSheet(TableSheet):
    title = "Quant Tracker"
    headers = ["Topic", "Concept", "Practice Sets", "Accuracy %", "Weak Area", "Next Review"]
    sample_rows = [
        ("Arithmetic", "Percentages", 3, 78, "Speed", ""),
        ("Algebra", "Linear equations", 2, 72, "Setup", ""),
    ]


class DilrTrackerSheet(TableSheet):
    title = "DILR Tracker"
    headers = ["Set Type", "Sets Attempted", "Solved", "Avg Time", "Accuracy %", "Notes"]
    sample_rows = [
        ("Arrangements", 4, 3, "14 min", 75, "Improve diagramming"),
        ("Tables", 3, 2, "16 min", 67, "Reduce rereads"),
    ]


class VarcTrackerSheet(TableSheet):
    title = "VARC Tracker"
    headers = ["Area", "Passages/Questions", "Accuracy %", "Review Theme", "Next Drill"]
    sample_rows = [
        ("Reading Comprehension", 3, 70, "Inference errors", "Dense passages"),
        ("Para Summary", 10, 80, "Option traps", "Timed set"),
    ]


class VocabularySheet(TableSheet):
    title = "Vocabulary"
    headers = ["Word", "Meaning", "Example", "Source", "Revision Count", "Confidence"]
    sample_rows = [
        ("Abate", "Reduce in intensity", "The pressure began to abate.", "Reading", 1, "Medium"),
        ("Lucid", "Clear and easy to understand", "A lucid explanation.", "Article", 2, "High"),
    ]


class RevisionTrackerSheet(TableSheet):
    title = "Revision Tracker"
    headers = ["Topic", "Revision 1", "Revision 2", "Revision 3", "Retention", "Action"]
    sample_rows = [
        ("Number systems", "", "", "", "Medium", "Rework errors"),
        ("Grammar rules", "", "", "", "High", "Maintain"),
    ]


class MockTestsSheet(TableSheet):
    title = "Mock Tests"
    headers = ["Mock", "Date", "Score", "Percentile", "Accuracy %", "Top Insight"]
    sample_rows = [
        ("Mock 1", "", 0, "", 0, "Capture baseline"),
        ("Mock 2", "", 0, "", 0, "Compare strategy"),
    ]


class AnalyticsSheet(TableSheet):
    title = "Analytics"
    headers = ["Metric", "Current", "Target", "Trend", "Interpretation"]
    sample_rows = [
        ("Weekly hours", 18, 20, "Up", "Close to target"),
        ("Mock accuracy", "68%", "80%", "Flat", "Needs review depth"),
    ]


class HabitsSheet(TableSheet):
    title = "Habits"
    headers = ["Habit", "Frequency", "Trigger", "Streak", "Status"]
    sample_rows = [
        ("Vocabulary review", "Daily", "After breakfast", 9, "Active"),
        ("Error log review", "3x/week", "After practice", 2, "Active"),
    ]


class NotesSheet(TableSheet):
    title = "Notes"
    headers = ["Date", "Category", "Note", "Linked Topic", "Follow-up"]
    sample_rows = [
        ("", "Strategy", "Review every incorrect mock question.", "Mock Tests", "Weekly"),
        ("", "Mindset", "Protect deep work blocks.", "Habits", "Daily"),
    ]


class InterviewPrepSheet(TableSheet):
    title = "Interview Prep"
    headers = ["Area", "Prompt", "Draft Status", "Evidence", "Next Step"]
    sample_rows = [
        ("SOP", "Why PGPEM?", "Draft", "Career goals", "Refine narrative"),
        ("STAR Story", "Leadership challenge", "Outline", "Project example", "Add metrics"),
    ]


class SettingsSheet(TableSheet):
    title = "Settings"
    headers = ["Setting", "Value", "Source", "Notes"]

    @property
    def sample_rows(self) -> list[tuple[str, str | int, str, str]]:
        return [
            ("Project", self.app_config.project_name, "YAML", "Workbook title"),
            ("Exam", self.app_config.exam.name, "YAML", "Target program"),
            ("Plan Days", self.app_config.exam.days, "YAML", "Used by planner"),
        ]


STANDARD_SHEET_CLASSES = [
    SmartGoalsSheet,
    Planner106DaySheet,
    DailyPlannerSheet,
    QuantTrackerSheet,
    DilrTrackerSheet,
    VarcTrackerSheet,
    VocabularySheet,
    RevisionTrackerSheet,
    MockTestsSheet,
    AnalyticsSheet,
    HabitsSheet,
    NotesSheet,
    InterviewPrepSheet,
    SettingsSheet,
]
