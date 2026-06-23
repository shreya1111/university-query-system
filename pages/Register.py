import streamlit as st
from textwrap import dedent
from features.auth.service import register_user, init_auth_state
from components.sidebar import render_sidebar
from styles.theme import COLORS

# Initialize authentication state
init_auth_state()

# If already logged in, redirect to home
if st.session_state.get("logged_in", False):
    st.switch_page("app.py")

# Page config
st.set_page_config(page_title="Register - UniQuery", page_icon="📝", layout="centered")

st.markdown(
    f"<div style='text-align: center; padding: 2rem 0;'>"
    f"<h1 style='color: {COLORS['text']};'>Register for UniQuery</h1>"
    f"<p style='color: {COLORS['muted']};'>Create your account</p>"
    f"</div>",
    unsafe_allow_html=True,
)

with st.container():
    st.markdown(
        f"<div style='max-width: 400px; margin: 0 auto; padding: 2rem; "
        f"background: {COLORS['card']}; border-radius: 18px; "
        f"border: 1px solid {COLORS['border_solid']};'>",
        unsafe_allow_html=True,
    )

    with st.form("register_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input(
            "Password", type="password", placeholder="Create a password"
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password",
        )
        role = st.selectbox(
            "Role",
            options=["Student", "Faculty", "Admin"],
            help="Select your role in the university",
        )
        department = st.selectbox(
            "Department",
            options=[
                "Admission",
                "Examination",
                "Hostel",
                "Finance",
                "Placement",
                "Scholarship",
                "General",
            ],
            help="Select your department",
        )
        submit_button = st.form_submit_button("Register", use_container_width=True)

        if submit_button:
            # Basic validation
            if not username or not email or not password or not confirm_password:
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                success, message = register_user(
                    username=username,
                    email=email,
                    password=password,
                    role=role,
                    department=department,
                )
                if success:
                    st.success(message)
                    # Optionally, automatically log in the user after registration
                    # For now, we'll just show success and let them login manually
                    st.info("You can now log in with your credentials")
                else:
                    st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)

# Link to login page
st.markdown(
    f"<div style='text-align: center; margin-top: 1.5rem;'>"
    f"<p style='color: {COLORS['muted']};'>"
    f"Already have an account? <a href='/Login' style='color: {COLORS['primary']}; text-decoration: none;'>Login here</a>"
    f"</p>"
    f"</div>",
    unsafe_allow_html=True,
)