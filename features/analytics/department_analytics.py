"""Department-level analytics."""
from core.database import _connect


def department_ticket_counts() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT department, COUNT(*) as count FROM tickets "
            "GROUP BY department ORDER BY count DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def department_performance() -> list[dict]:
    """Resolved / pending / in-progress per department."""
    sql = """
    SELECT
        department,
        COUNT(*) as total,
        SUM(CASE WHEN status='Resolved'    THEN 1 ELSE 0 END) as resolved,
        SUM(CASE WHEN status='Pending'     THEN 1 ELSE 0 END) as pending,
        SUM(CASE WHEN status='In Progress' THEN 1 ELSE 0 END) as in_progress
    FROM tickets
    GROUP BY department
    ORDER BY total DESC
    """
    with _connect() as conn:
        return [dict(r) for r in conn.execute(sql).fetchall()]


def most_active_department() -> str:
    with _connect() as conn:
        row = conn.execute(
            "SELECT department FROM tickets "
            "GROUP BY department ORDER BY COUNT(*) DESC LIMIT 1"
        ).fetchone()
    return row["department"] if row else "N/A"


def average_resolution_time() -> list[dict]:
    """Average days open per department (unresolved tickets)."""
    sql = """
    SELECT department,
           ROUND(AVG(JULIANDAY('now') - JULIANDAY(created_at)), 1) as avg_days_open
    FROM tickets
    WHERE status != 'Resolved'
    GROUP BY department
    ORDER BY avg_days_open DESC
    """
    with _connect() as conn:
        return [dict(r) for r in conn.execute(sql).fetchall()]
