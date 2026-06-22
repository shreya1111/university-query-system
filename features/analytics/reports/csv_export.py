"""CSV export helpers — return bytes for st.download_button."""
import io
import csv
from features.analytics.ticket_analytics import get_all_tickets_raw
from features.analytics.department_analytics import department_performance
from features.analytics.sentiment_analytics import sentiment_distribution, intent_distribution
from features.analytics.resolution_analytics import resolution_summary


def _to_csv_bytes(rows: list[dict]) -> bytes:
    if not rows:
        return b"No data available\n"
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8")


def export_all_tickets() -> bytes:
    return _to_csv_bytes(get_all_tickets_raw())


def export_department_report() -> bytes:
    return _to_csv_bytes(department_performance())


def export_sentiment_report() -> bytes:
    return _to_csv_bytes(sentiment_distribution())


def export_analytics_csv() -> bytes:
    """Combined analytics snapshot CSV."""
    rows = []
    for d in intent_distribution():
        rows.append({"category": "Intent", "label": d["intent"], "count": d["count"]})
    for d in sentiment_distribution():
        rows.append({"category": "Sentiment", "label": d["sentiment"], "count": d["count"]})
    for d in department_performance():
        rows.append({"category": "Department", "label": d["department"],
                     "count": d["total"]})
    return _to_csv_bytes(rows) if rows else b"No analytics data\n"
