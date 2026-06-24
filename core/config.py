from pathlib import Path

# Project root (two levels up from this file: core/ -> project root)
BASE_DIR = Path(__file__).resolve().parent.parent

APP_TITLE = "University Query Management System"
APP_ICON = "🎓"

# Database paths – absolute for reliability
DB_PATH = str(BASE_DIR / "database" / "university.db")
SCHEMA_PATH = str(BASE_DIR / "database" / "schema.sql")

DEPARTMENTS = ["Admission","Examination","Hostel","Finance","Placement","Scholarship","General"]
PRIORITIES  = ["Low","Medium","High"]
STATUSES    = ["Pending","In Progress","Resolved"]

# New design tokens live in styles/theme.py
# THEME kept here for backward-compatibility with any remaining references.
THEME = {
    "primary":      "#6366F1",
    "bg":           "#071129",
    "secondary_bg": "#0F172A",
    "text":         "#F8FAFC",
    "muted":        "#94A3B8",
    "border":       "rgba(255,255,255,0.08)",
    "border_solid": "#1E2D4A",
    "success":      "#22C55E",
    "warning":      "#F59E0B",
    "danger":       "#EF4444",
}

PRIORITY_COLORS = {"Low": "#22C55E", "Medium": "#F59E0B", "High": "#EF4444"}
STATUS_COLORS   = {"Pending": "#F59E0B", "In Progress": "#6366F1", "Resolved": "#22C55E"}

