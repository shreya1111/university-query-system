"""
Student Satisfaction Analytics.
Satisfaction scores are derived from ticket sentiment since no explicit
rating column exists. Positive=5, Neutral=3, Negative=1.
Extend by adding a 'rating' column to tickets when collecting real scores.
"""
from core.database import _connect

_SCORE_MAP = {"Positive": 5, "Neutral": 3, "Negative": 1}


def _all_scores() -> list[int]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT sentiment FROM tickets WHERE sentiment != ''"
        ).fetchall()
    return [_SCORE_MAP[r[0]] for r in rows if r[0] in _SCORE_MAP]


def average_satisfaction_score() -> float:
    scores = _all_scores()
    return round(sum(scores) / len(scores), 2) if scores else 0.0


def rating_distribution() -> dict[str, int]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT sentiment, COUNT(*) as count FROM tickets "
            "WHERE sentiment != '' GROUP BY sentiment"
        ).fetchall()
    return {r[0]: r[1] for r in rows}


def satisfaction_trend() -> list[dict]:
    """Monthly average satisfaction score."""
    sql = """
    SELECT
        STRFTIME('%Y-%m', created_at) as month,
        AVG(CASE sentiment
            WHEN 'Positive' THEN 5
            WHEN 'Neutral'  THEN 3
            WHEN 'Negative' THEN 1
            ELSE NULL END) as avg_score,
        COUNT(*) as count
    FROM tickets
    WHERE sentiment != ''
    GROUP BY STRFTIME('%Y-%m', created_at)
    ORDER BY month
    """
    with _connect() as conn:
        rows = conn.execute(sql).fetchall()
    return [
        {"month": r[0], "avg_score": round(r[1], 2), "count": r[2]}
        for r in rows
    ]


def top_issues() -> list[dict]:
    """Most common intents/issues by ticket count."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT intent, COUNT(*) as count FROM tickets "
            "WHERE intent != '' GROUP BY intent ORDER BY count DESC LIMIT 10"
        ).fetchall()
    return [dict(r) for r in rows]
