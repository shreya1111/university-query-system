import streamlit as st
from typing import Optional, Tuple, Dict
from .repository import (
    create_user,
    get_user_by_username,
    get_user_by_email,
    get_user_by_id,
)
from .password_utils import check_password
from .session import set_session, clear_session, init_auth_state


def register_user(username: str, email: str, password: str, role: str, department: str) -> tuple[bool, str]:
    """
    Register a new user.

    Args:
        username: The desired username.
        email: The user's email address.
        password: The plain-text password.
        role: The role (Student, Faculty, Admin).
        department: The department the user belongs to.

    Returns:
        A tuple (success, message). If successful, success is True and message is empty.
        If unsuccessful, success is False and message contains an error description.
    """
    # Initialize auth state (ensures session state variables exist)
    init_auth_state()

    # Basic validation
    if not username or not email or not password or not role or not department:
        return False, "All fields are required"

    if role not in ("Student", "Faculty", "Admin"):
        return False, "Invalid role"

    try:
        user_id = create_user(username, email, password, role, department)
        return True, f"User registered successfully with ID {user_id}"
    except ValueError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Registration failed: {str(e)}"


def login_user(username: str, password: str) -> tuple[bool, str]:
    """
    Authenticate a user and set up the session.

    Args:
        username: The username to authenticate.
        password: The plain-text password to check.

    Returns:
        A tuple (success, message). If successful, success is True and message is empty.
        If unsuccessful, success is False and message contains an error description.
    """
    init_auth_state()

    if not username or not password:
        return False, "Username and password are required"

    # Get user by username
    user = get_user_by_username(username)
    if not user:
        return False, "Invalid username or password"

    # Verify password
    if not check_password(password, user["password_hash"]):
        return False, "Invalid username or password"

    # Set session
    set_session(
        user_id=user["user_id"],
        username=user["username"],
        role=user["role"],
        department=user["department"],
    )
    return True, "Login successful"


def logout_user() -> None:
    """
    Log out the current user by clearing the session.
    """
    clear_session()


def get_current_user() -> Optional[Dict]:
    """
    Get the currently logged-in user's information from session state.

    Returns:
        A dictionary with user information if logged in, None otherwise.
    """
    init_auth_state()
    if not st.session_state.get("logged_in", False):
        return None
    return {
        "user_id": st.session_state.get("user_id"),
        "username": st.session_state.get("username"),
        "role": st.session_state.get("role"),
        "department": st.session_state.get("department"),
    }