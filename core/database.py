import sqlite3
import os
import re
from html import unescape
from html.parser import HTMLParser
from typing import Optional
from core.config import DB_PATH, SCHEMA_PATH


class _HTMLStripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self._parts.append(data)

    def get_text(self) -> str:
        return "".join(self._parts)


def _strip_html(value: str) -> str:
    if not value:
        return ""
    stripped = _HTMLStripper()
    stripped.feed(value)
    stripped.close()
    text = unescape(stripped.get_text())
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def initialize_database() -> None:
    if not os.path.exists(SCHEMA_PATH):
        return
    with _connect() as conn:
        with open(SCHEMA_PATH) as f:
            conn.executescript(f.read())
        # Phase 2B: migrate existing DB — add AI columns if absent
        existing = {r[1] for r in conn.execute("PRAGMA table_info(tickets)").fetchall()}
        for col, definition in [
            ("intent",     "TEXT DEFAULT ''"),
            ("summary",    "TEXT DEFAULT ''"),
            ("sentiment",  "TEXT DEFAULT ''"),
            ("auto_reply", "TEXT DEFAULT ''"),
        ]:
            if col not in existing:
                conn.execute(f"ALTER TABLE tickets ADD COLUMN {col} {definition}")
        migrate_ticket_queries_to_plain_text(conn)


def migrate_ticket_queries_to_plain_text(conn: sqlite3.Connection) -> None:
    rows = conn.execute("SELECT ticket_id, query FROM tickets").fetchall()
    for row in rows:
        clean_query = _strip_html(row["query"])
        if clean_query != row["query"]:
            conn.execute(
                "UPDATE tickets SET query = ? WHERE ticket_id = ?",
                (clean_query, row["ticket_id"]),
            )


def _normalize_query(query: str) -> str:
    return _strip_html(query)


def create_ticket(student_name: str, query: str, department: str, priority: str) -> int:
    sql = """
    INSERT INTO tickets (student_name, query, department, priority, status)
    VALUES (?, ?, ?, ?, 'Pending')
    """
    with _connect() as conn:
        cur = conn.execute(sql, (student_name, _normalize_query(query), department, priority))
        _add_notification(conn, f"New ticket #{cur.lastrowid} raised by {student_name}.")
        return cur.lastrowid


def create_ticket_with_ai(
    student_name: str,
    query: str,
    department: str,
    priority: str,
    intent: str,
    summary: str,
    sentiment: str,
    auto_reply: str,
) -> int:
    sql = """
    INSERT INTO tickets
        (student_name, query, department, priority, status,
         intent, summary, sentiment, auto_reply)
    VALUES (?, ?, ?, ?, 'Pending', ?, ?, ?, ?)
    """
    with _connect() as conn:
        cur = conn.execute(sql, (
            student_name, _normalize_query(query), department, priority,
            intent, summary, sentiment, auto_reply,
        ))
        _add_notification(conn, f"New ticket #{cur.lastrowid} raised by {student_name}.")
        return cur.lastrowid


def get_all_tickets(
    department: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
) -> list[dict]:
    conditions, params = [], []
    if department:
        conditions.append("department = ?"); params.append(department)
    if priority:
        conditions.append("priority = ?"); params.append(priority)
    if status:
        conditions.append("status = ?"); params.append(status)
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    sql = f"SELECT * FROM tickets {where} ORDER BY created_at DESC"
    with _connect() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def get_ticket_by_id(ticket_id: int) -> Optional[dict]:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
        return dict(row) if row else None


def update_ticket_status(ticket_id: int, status: str) -> None:
    with _connect() as conn:
        conn.execute("UPDATE tickets SET status = ? WHERE ticket_id = ?", (status, ticket_id))
        _add_notification(conn, f"Ticket #{ticket_id} status updated to '{status}'.")


def get_stats() -> dict:
    with _connect() as conn:
        total    = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        pending  = conn.execute("SELECT COUNT(*) FROM tickets WHERE status='Pending'").fetchone()[0]
        resolved = conn.execute("SELECT COUNT(*) FROM tickets WHERE status='Resolved'").fetchone()[0]
        in_prog  = conn.execute("SELECT COUNT(*) FROM tickets WHERE status='In Progress'").fetchone()[0]
    return {"total": total, "pending": pending, "resolved": resolved, "in_progress": in_prog}


def get_dept_distribution() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT department, COUNT(*) as count FROM tickets GROUP BY department"
        ).fetchall()
        return [dict(r) for r in rows]


def get_priority_distribution() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT priority, COUNT(*) as count FROM tickets GROUP BY priority"
        ).fetchall()
        return [dict(r) for r in rows]


def _add_notification(conn: sqlite3.Connection, message: str) -> None:
    conn.execute("INSERT INTO notifications (message) VALUES (?)", (message,))
