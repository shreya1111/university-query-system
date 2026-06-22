"""Resolution time analytics."""
from core.database import _connect


def resolution_summary() -> dict:
    with _connect() as conn:
        total    = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        resolved = conn.execute("SELECT COUNT(*) FROM tickets WHERE status='Resolved'").fetchone()[0]
        avg_open = conn.execute(
            "SELECT ROUND(AVG(JULIANDAY('now')-JULIANDAY(created_at)),1) FROM tickets"
        ).fetchone()[0] or 0.0
    rate = round((resolved / total * 100), 1) if total else 0.0
    return {"total": total, "resolved": resolved, "resolution_rate": rate,
            "avg_days_open": avg_open}


def fastest_department() -> str:
    with _connect() as conn:
        row = conn.execute("""
            SELECT department,
                   AVG(JULIANDAY('now')-JULIANDAY(created_at)) as avg_days
            FROM tickets WHERE status='Resolved'
            GROUP BY department ORDER BY avg_days ASC LIMIT 1
        """).fetchone()
    return row["department"] if row else "N/A"


def slowest_department() -> str:
    with _connect() as conn:
        row = conn.execute("""
            SELECT department,
                   AVG(JULIANDAY('now')-JULIANDAY(created_at)) as avg_days
            FROM tickets WHERE status!='Resolved'
            GROUP BY department ORDER BY avg_days DESC LIMIT 1
        """).fetchone()
    return row["department"] if row else "N/A"


def resolution_trends() -> list[dict]:
    sql = """
    SELECT DATE(created_at) as day,
           SUM(CASE WHEN status='Resolved' THEN 1 ELSE 0 END) as resolved,
           COUNT(*) as total
    FROM tickets
    WHERE created_at >= DATE('now','-30 days')
    GROUP BY DATE(created_at) ORDER BY day
    """
    with _connect() as conn:
        return [dict(r) for r in conn.execute(sql).fetchall()]
