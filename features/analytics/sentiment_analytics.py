"""Sentiment distribution analytics."""
from core.database import _connect


def sentiment_distribution() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT sentiment, COUNT(*) as count FROM tickets "
            "WHERE sentiment != '' GROUP BY sentiment ORDER BY count DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def sentiment_percentages() -> dict:
    dist = sentiment_distribution()
    total = sum(d["count"] for d in dist)
    if not total:
        return {"Positive": 0, "Neutral": 0, "Negative": 0}
    return {d["sentiment"]: round(d["count"] / total * 100, 1) for d in dist}


def intent_distribution() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT intent, COUNT(*) as count FROM tickets "
            "WHERE intent != '' GROUP BY intent ORDER BY count DESC"
        ).fetchall()
        return [dict(r) for r in rows]
