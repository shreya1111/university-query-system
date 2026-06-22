"""Notification service — SQLite-backed."""
from core.database import _connect


def get_notifications(limit: int = 50) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM notifications ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def create_notification(message: str) -> None:
    with _connect() as conn:
        conn.execute("INSERT INTO notifications (message) VALUES (?)", (message,))


def mark_as_read(notification_id: int | None = None) -> None:
    """
    Placeholder — the notifications table has no 'read' column yet.
    Pass None to mark all as read conceptually.
    Extend the DB schema with ALTER TABLE when needed.
    """
    pass  # no-op until schema is extended


def unread_count() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM notifications").fetchone()[0]
