import os
import streamlit as st
from features.auth.session import init_auth_state, get_session


def require_login() -> None:
    """
    Check if the user is logged in. If not, redirect to the login page.
    This function should be called at the top of each protected page.
    It allows access to the login and registration pages without authentication.
    """
    # Initialize auth state to ensure session variables exist
    init_auth_state()
    session = get_session()
    logged_in = session.get("logged_in", False)

    # Get the current script filename
    current_file = os.path.basename(__file__)

    # Define which pages are accessible without login
    public_pages = {"Login.py", "Register.py"}

    # If not logged in and the current page is not a public page, redirect to login
    if not logged_in and current_file not in public_pages:
        st.switch_page("pages/Login.py")