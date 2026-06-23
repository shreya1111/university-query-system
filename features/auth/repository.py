import sqlite3
from typing import Optional, Dict
from core.database import _connect
from .password_utils import hash_password


def create_user(username: str, email: str, password: str, role: str, department: str) -> int:
    """
    Create a new user in the database.

    Args:
        username: The username (must be unique).
        email: The email address (must be unique).
        password: The plain-text password to be hashed.
        role: The role (Student, Faculty, Admin).
        department: The department the user belongs to.

    Returns:
        The newly created user's ID.

    Raises:
        ValueError: If the username or email already exists.
    """
    hashed_password = hash_password(password)
    sql = """
    INSERT INTO users (username, email, password_hash, role, department)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        with _connect() as conn:
            cursor = conn.execute(
                sql,
                (username, email, hashed_password, role, department),
            )
            return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            raise ValueError("Username already exists")
        elif "email" in str(e):
            raise ValueError("Email already exists")
        else:
            raise ValueError("User with similar details already exists")


def get_user_by_username(username: str) -> Optional[Dict]:
    """
    Retrieve a user by their username.

    Args:
        username: The username to search for.

    Returns:
        A dictionary representing the user, or None if not found.
    """
    sql = "SELECT * FROM users WHERE username = ?"
    with _connect() as conn:
        cursor = conn.execute(sql, (username,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_user_by_email(email: str) -> Optional[Dict]:
    """
    Retrieve a user by their email address.

    Args:
        email: The email address to search for.

    Returns:
        A dictionary representing the user, or None if not found.
    """
    sql = "SELECT * FROM users WHERE email = ?"
    with _connect() as conn:
        cursor = conn.execute(sql, (email,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int) -> Optional[Dict]:
    """
    Retrieve a user by their ID.

    Args:
        user_id: The user's ID.

    Returns:
        A dictionary representing the user, or None if not found.
    """
    sql = "SELECT * FROM users WHERE user_id = ?"
    with _connect() as conn:
        cursor = conn.execute(sql, (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_user_password(email: str, password_hash: str) -> bool:
    """
    Update a user's password hash, looked up by email.

    Args:
        email: The user's email address.
        password_hash: The new hashed password.

    Returns:
        True if a row was updated, False otherwise.
    """
    sql = "UPDATE users SET password_hash = ? WHERE email = ?"
    with _connect() as conn:
        cursor = conn.execute(sql, (password_hash, email))
        return cursor.rowcount > 0