"""
PDF report generator using only the stdlib + reportlab (if available).
Falls back to a plain text report if reportlab is not installed.
"""
import io
import os
from datetime import datetime
from features.analytics.ticket_analytics import get_all_tickets_raw, get_total_tickets
from features.analytics.department_analytics import department_performance
from features.analytics.resolution_analytics import resolution_summary

REPORTS_DIR = "reports"


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def generate_summary_report() -> bytes:
    """Return PDF bytes (or plain-text bytes as fallback)."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle)
        from reportlab.lib.styles import getSampleStyleSheet
        return _build_pdf_reportlab()
    except ImportError:
        return _build_text_report()


def _build_text_report() -> bytes:
    stats  = resolution_summary()
    depts  = department_performance()
    lines  = [
        "UNIVERSITY QUERY MANAGEMENT SYSTEM",
        f"Report generated: {datetime.now().strftime('%d %b %Y %H:%M')}",
        "=" * 50,
        f"Total Tickets   : {stats['total']}",
        f"Resolved        : {stats['resolved']}",
        f"Resolution Rate : {stats['resolution_rate']}%",
        f"Avg Days Open   : {stats['avg_days_open']}",
        "",
        "DEPARTMENT BREAKDOWN",
        "-" * 30,
    ]
    for d in depts:
        lines.append(
            f"  {d['department']:<25} total={d['total']}  "
            f"resolved={d['resolved']}  pending={d['pending']}"
        )
    return "\n".join(lines).encode("utf-8")


def _build_pdf_reportlab() -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet

    buf    = io.BytesIO()
    doc    = SimpleDocTemplate(buf, pagesize=A4)
    styles = getSampleStyleSheet()
    story  = []

    story.append(Paragraph("University Query Management System", styles["Title"]))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %b %Y %H:%M')}", styles["Normal"]))
    story.append(Spacer(1, 20))

    stats = resolution_summary()
    story.append(Paragraph("Summary", styles["Heading2"]))
    summary_data = [
        ["Metric", "Value"],
        ["Total Tickets",   str(stats["total"])],
        ["Resolved",        str(stats["resolved"])],
        ["Resolution Rate", f"{stats['resolution_rate']}%"],
        ["Avg Days Open",   str(stats["avg_days_open"])],
    ]
    t = Table(summary_data, colWidths=[200, 200])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#6366F1")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f0f0f0")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    story.append(Paragraph("Department Breakdown", styles["Heading2"]))
    dept_data = [["Department","Total","Resolved","Pending","In Progress"]]
    for d in department_performance():
        dept_data.append([
            d["department"], str(d["total"]),
            str(d["resolved"]), str(d["pending"]), str(d["in_progress"]),
        ])
    t2 = Table(dept_data, colWidths=[150,60,70,70,80])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#6366F1")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f0f0f0")]),
    ]))
    story.append(t2)
    doc.build(story)
    return buf.getvalue()


def save_report(content: bytes, name: str = "report") -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    ext  = "pdf" if content[:4] == b"%PDF" else "txt"
    path = os.path.join(REPORTS_DIR, f"{name}_{_timestamp()}.{ext}")
    with open(path, "wb") as f:
        f.write(content)
    return path
