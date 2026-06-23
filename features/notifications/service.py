"""
Service layer for notifications module.
Handles notification logic.
"""
from .repository import (
    get_notifications,
    create_notification,
    mark_as_read,
    clear_notifications,
    unread_count,
)