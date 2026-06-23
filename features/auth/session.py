import streamlit as st
from typing import Dict, Any


def init_auth_state() -> None:
    """
    Initialize authentication-related session state variables if they don't exist.
    """
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "department" not in st.session_state:
        st.session_state.department = None


def set_session(user_id: int, username: str, role: str, department: str) -> None:
    """
    Set the session state for a logged-in user.

    Args:
        user_id: The user's ID.
        username: The user's username.
        role: The user's role (Student, Faculty, Admin).
        department: The user's department.
    """
    st.session_state.logged_in = True
    st.session_state.user_id = user_id
    st.session_state.username = username
    st.session_state.role = role
    st.session_state.department = department


def clear_session() -> None:
    """
    Clear the session state, effectively logging out the user.
    """
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.department = None


def get_session() -> Dict[str, Any]:
    """
    Get the current session state as a dictionary.

    Returns:
        A dictionary containing the session state variables.
    """
    return {
        "logged_in": st.session_state.get("logged_in", False),
        "user_id": st.session_state.get("user_id"),
        "username": st.session_state.get("username"),
        "role": st.session_state.get("role"),
        "department": st.session_state.get("department"),
    }