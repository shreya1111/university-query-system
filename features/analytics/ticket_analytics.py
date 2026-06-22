"""Ticket-level analytics queries against SQLite."""
import sqlite3
from core.database import _connect


def get_total_tickets() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]


def get_pending_tickets() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM tickets WHERE status='Pending'").fetchone()[0]


def get_resolved_tickets() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM tickets WHERE status='Resolved'").fetchone()[0]


def get_high_priority_tickets() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM tickets WHERE priority='High'").fetchone()[0]


def get_in_progress_tickets() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM tickets WHERE status='In Progress'").fetchone()[0]


def get_ticket_trends() -> list[dict]:
    """Return daily ticket counts for the last 30 days."""
    sql = """
    SELECT DATE(created_at) as day, COUNT(*) as count
    FROM tickets
    WHERE created_at >= DATE('now', '-30 days')
    GROUP BY DATE(created_at)
    ORDER BY day
    """
    with _connect() as conn:
        return [dict(r) for r in conn.execute(sql).fetchall()]


def get_all_tickets_raw() -> list[dict]:
    with _connect() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM tickets ORDER BY created_at DESC"
        ).fetchall()]
