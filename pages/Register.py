import streamlit as st
from textwrap import dedent

from features.auth.service import register_user, init_auth_state
from styles.theme import COLORS
from styles.custom_css import inject_css

# Initialize authentication state
init_auth_state()

# If already logged in, redirect to home
if st.session_state.get("logged_in", False):
    st.switch_page("app.py")

st.set_page_config(
    page_title="Register - UniQuery",
    page_icon="📝",
    layout="centered",
)

# Apply the global dark theme + hide Streamlit's default chrome/sidebar nav
inject_css()
st.markdown("<style>[data-testid='stSidebar']{display:none !important;}</style>",
            unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────
st.markdown(dedent(f"""
<div style="text-align:center;padding:1.2rem 0 1.6rem;">
    <div style="display:inline-flex;align-items:center;justify-content:center;
        width:64px;height:64px;border-radius:18px;font-size:2rem;margin-bottom:.7rem;
        background:linear-gradient(135deg,{COLORS['accent']},{COLORS['primary']});">
        📝
    </div>
    <h1 style="color:{COLORS['text']};font-size:1.7rem;font-weight:800;margin:0;">
        Create your account
    </h1>
    <p style="color:{COLORS['muted']};font-size:.92rem;margin:.3rem 0 0;">
        Join UniQuery to raise and track your queries
    </p>
</div>
"""), unsafe_allow_html=True)

# ── Registration form ─────────────────────────────────────────────────────
with st.form("register_form"):
    username = st.text_input("Username", placeholder="Choose a username")
    email = st.text_input("Email", placeholder="you@university.edu")
    password = st.text_input(
        "Password", type="password", placeholder="At least 6 characters"
    )
    confirm_password = st.text_input(
        "Confirm Password", type="password", placeholder="Re-enter password"
    )
    role = st.selectbox(
        "Role",
        options=["Student", "Faculty", "Admin"],
        help="Select your role in the university",
    )
    department = st.selectbox(
        "Department",
        options=[
            "Admission", "Examination", "Hostel", "Finance",
            "Placement", "Scholarship", "General",
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
                st.info("Redirecting to login…")
                st.switch_page("pages/Login.py")
            else:
                st.error(message)

# ── Footer link back to login ────────────────────────────────────────────
# NOTE: <a href="/Login"> does NOT work in Streamlit; use a button instead.
if st.button("Already have an account? Sign in", key="to_login",
             use_container_width=True):
    st.switch_page("pages/Login.py")
