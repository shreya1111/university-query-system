"""
Repository layer for notifications module.
Handles data access for notifications.
"""
from typing import List, Dict, Any, Optional
from core.database import _connect


def get_notifications(limit: int = 50, unread_only: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch notifications from the database.
    :param limit: Maximum number of notifications to return
    :param unread_only: If True, return only unread notifications
    :return: List of notification dictionaries
    """
    with _connect() as conn:
        if unread_only:
            rows = conn.execute(
                "SELECT * FROM notifications WHERE read = 0 ORDER BY timestamp DESC LIMIT ?", (limit,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM notifications ORDER BY timestamp DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in rows]


def create_notification(message: str) -> None:
    """
    Create a new notification.
    :param message: Notification message
    """
    with _connect() as conn:
        conn.execute("INSERT INTO notifications (message) VALUES (?)", (message,))


def mark_as_read(notification_id: Optional[int] = None) -> None:
    """
    Mark notification(s) as read.
    :param notification_id: If provided, mark only this notification as read.
                            If None, mark all notifications as read.
    """
    with _connect() as conn:
        if notification_id is None:
            conn.execute("UPDATE notifications SET read = 1")
        else:
            conn.execute("UPDATE notifications SET read = 1 WHERE notification_id = ?", (notification_id,))


def clear_notifications() -> None:
    """
    Delete all notifications from the database.
    """
    with _connect() as conn:
        conn.execute("DELETE FROM notifications")


def unread_count() -> int:
    """
    Get the number of unread notifications.
    :return: Count of unread notifications
    """
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM notifications WHERE read = 0").fetchone()[0]