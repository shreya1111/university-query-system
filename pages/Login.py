import streamlit as st
from textwrap import dedent
from features.auth.service import login_user, logout_user, init_auth_state
from components.sidebar import render_sidebar
from styles.theme import COLORS

# Initialize authentication state
init_auth_state()

# If already logged in, redirect to home
if st.session_state.get("logged_in", False):
    st.switch_page("app.py")

# Page config (optional, but we can set title)
st.set_page_config(page_title="Login - UniQuery", page_icon="🔐", layout="centered")

# Custom CSS for login page (optional, but we can reuse existing styles)
# We'll just use the existing theme colors

# Center the login form
st.markdown(
    f"<div style='text-align: center; padding: 2rem 0;'>"
    f"<h1 style='color: {COLORS['text']};'>UniQuery Login</h1>"
    f"<p style='color: {COLORS['muted']};'>Sign in to your account</p>"
    f"</div>",
    unsafe_allow_html=True,
)

# Create a container for the form with a max-width
with st.container():
    st.markdown(
        f"<div style='max-width: 400px; margin: 0 auto; padding: 2rem; "
        f"background: {COLORS['card']}; border-radius: 18px; "
        f"border: 1px solid {COLORS['border_solid']};'>",
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input(
            "Password", type="password", placeholder="Enter your password"
        )
        submit_button = st.form_submit_button("Login", use_container_width=True)

        if submit_button:
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                success, message = login_user(username, password)
                if success:
                    st.success(message)
                    # Redirect to home after successful login
                    st.switch_page("app.py")
                else:
                    st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)

# Add a link to register page
st.markdown(
    f"<div style='text-align: center; margin-top: 1.5rem;'>"
    f"<p style='color: {COLORS['muted']};'>"
    f"Don't have an account? <a href='/Register' style='color: {COLORS['primary']}; text-decoration: none;'>Register here</a>"
    f"</p>"
    f"</div>",
    unsafe_allow_html=True,
)