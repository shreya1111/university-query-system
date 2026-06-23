import streamlit as st
from textwrap import dedent

from features.auth.service import (
    request_password_reset,
    verify_otp,
    reset_password,
    init_auth_state,
)
from components.sidebar import render_sidebar
from styles.theme import COLORS
from styles.custom_css import inject_css

# Initialize auth state
init_auth_state()

# If the user is already logged in, redirect to home
if st.session_state.get("logged_in", False):
    st.switch_page("app.py")

st.set_page_config(
    page_title="Forgot Password - UniQuery",
    page_icon="🔑",
    layout="centered",
)

inject_css()
render_sidebar()

# ── Step state ────────────────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.email = ""

STEP_TITLES = {
    1: ("Request Reset", "Enter your registered email to receive a code."),
    2: ("Verify Code", "Enter the 6-digit code we sent to your email."),
    3: ("New Password", "Choose a new password for your account."),
}

# ── Header ────────────────────────────────────────────────────────────────
title, subtitle = STEP_TITLES[st.session_state.step]
st.markdown(dedent(f"""
<div style="text-align:center;padding:1rem 0 1.4rem;">
    <div style="font-size:2.4rem;">🔑</div>
    <h1 style="color:{COLORS['text']};font-size:1.6rem;font-weight:800;margin:.4rem 0 .2rem;">
        {title}
    </h1>
    <p style="color:{COLORS['muted']};font-size:.9rem;margin:0;">{subtitle}</p>
</div>
"""), unsafe_allow_html=True)

# ── Step progress dots ───────────────────────────────────────────────────
_dot_active = COLORS["primary"]
_dot_done = COLORS["primary"]
_dot_idle = COLORS["border_solid"]
dots = "".join(
    f'<span style="display:inline-block;width:9px;height:9px;border-radius:50%;'
    f'margin:0 5px;background:{_dot_done if i + 1 <= st.session_state.step else _dot_idle};"></span>'
    for i in range(3)
)
st.markdown(
    f'<div style="text-align:center;margin-bottom:1.6rem;">{dots}</div>',
    unsafe_allow_html=True,
)
_ = _dot_active  # reserved for future use

# ── STEP 1: Request OTP ──────────────────────────────────────────────────
if st.session_state.step == 1:
    with st.form("request_otp_form"):
        email = st.text_input(
            "Email address",
            value=st.session_state.email,
            placeholder="you@university.edu",
        )
        submitted = st.form_submit_button("Send Code", use_container_width=True)
        if submitted:
            if not email:
                st.error("Please enter your email address.")
            else:
                success, message = request_password_reset(email)
                if success:
                    st.success(message)
                    st.session_state.email = email
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error(message)

# ── STEP 2: Verify OTP ───────────────────────────────────────────────────
elif st.session_state.step == 2:
    with st.form("verify_otp_form"):
        otp = st.text_input("6-digit code", placeholder="e.g. 123456")
        col_a, col_b = st.columns([1, 1])
        with col_a:
            back = st.form_submit_button("← Back", use_container_width=True)
        with col_b:
            submitted = st.form_submit_button("Verify", use_container_width=True)

        if back:
            st.session_state.step = 1
            st.rerun()
        if submitted:
            if not otp:
                st.error("Please enter the code.")
            else:
                success, message = verify_otp(st.session_state.email, otp)
                if success:
                    st.success(message)
                    st.session_state.otp = otp
                    st.session_state.step = 3
                    st.rerun()
                else:
                    st.error(message)

# ── STEP 3: New password ─────────────────────────────────────────────────
elif st.session_state.step == 3:
    with st.form("reset_password_form"):
        new_password = st.text_input("New password", type="password")
        confirm_password = st.text_input(
            "Confirm new password", type="password"
        )
        col_a, col_b = st.columns([1, 1])
        with col_a:
            back = st.form_submit_button("← Back", use_container_width=True)
        with col_b:
            submitted = st.form_submit_button(
                "Reset Password", use_container_width=True
            )

        if back:
            st.session_state.step = 2
            st.rerun()
        if submitted:
            if not new_password or not confirm_password:
                st.error("Please enter and confirm the new password.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = reset_password(
                    st.session_state.email,
                    st.session_state.otp,
                    new_password,
                )
                if success:
                    st.success(message)
                    # Clean up reset state
                    for key in ("step", "email", "otp"):
                        st.session_state.pop(key, None)
                    st.info("Redirecting to login…")
                    st.switch_page("pages/Login.py")
                else:
                    st.error(message)

# ── Footer link back to login ────────────────────────────────────────────
if st.button("← Back to Login", key="to_login", use_container_width=False):
    st.switch_page("pages/Login.py")
