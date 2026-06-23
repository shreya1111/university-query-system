import streamlit as st
from textwrap import dedent

from features.auth.service import login_user, init_auth_state
from styles.theme import COLORS
from styles.custom_css import inject_css

# Initialize authentication state
init_auth_state()

# If already logged in, redirect to home
if st.session_state.get("logged_in", False):
    st.switch_page("app.py")

st.set_page_config(
    page_title="Login - UniQuery",
    page_icon="🔐",
    layout="centered",
)

# Apply the global dark theme + hide Streamlit's default chrome/sidebar nav
inject_css()
# Minimal sidebar (no nav links for guests beyond what render_sidebar shows)
st.markdown("<style>[data-testid='stSidebar']{display:none !important;}</style>",
            unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────
st.markdown(dedent(f"""
<div style="text-align:center;padding:1.2rem 0 1.6rem;">
    <div style="display:inline-flex;align-items:center;justify-content:center;
        width:64px;height:64px;border-radius:18px;font-size:2rem;margin-bottom:.7rem;
        background:linear-gradient(135deg,{COLORS['primary']},{COLORS['accent']});">
        🎓
    </div>
    <h1 style="color:{COLORS['text']};font-size:1.7rem;font-weight:800;margin:0;">
        Welcome to UniQuery
    </h1>
    <p style="color:{COLORS['muted']};font-size:.92rem;margin:.3rem 0 0;">
        Sign in to your account
    </p>
</div>
"""), unsafe_allow_html=True)

# ── Login form ─────────────────────────────────────────────────────────────
with st.form("login_form", clear_on_submit=False):
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input(
        "Password", type="password", placeholder="Enter your password"
    )
    submit_button = st.form_submit_button(
        "Sign In", use_container_width=True, type="primary"
    )

    if submit_button:
        if not username or not password:
            st.error("Please enter both username and password")
        else:
            success, message = login_user(username, password)
            if success:
                st.success(message)
                st.switch_page("app.py")
            else:
                st.error(message)

# ── Secondary actions: forgot password + register ────────────────────────
# NOTE: <a href="/Page"> does NOT work in Streamlit; use buttons instead.
col_forgot, col_register = st.columns([1, 1])
with col_forgot:
    if st.button("Forgot password?", key="forgot_pwd",
                 use_container_width=True, help="Reset your password via email"):
        st.switch_page("pages/Forgot_Password.py")
with col_register:
    if st.button("Create account", key="to_register", use_container_width=True):
        st.switch_page("pages/Register.py")
