import streamlit as st
from html import escape
from textwrap import dedent
from styles.theme import COLORS
from features.auth.session import init_auth_state, get_session


def _section_label(text: str) -> None:
    safe_text = escape(str(text))
    st.markdown(
        f'<div style="color:{COLORS["muted"]};font-size:.68rem;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:.1em;"'
        f'padding:.9rem 1rem .25rem;margin:0;">{safe_text}</div>',
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    # Initialize authentication state
    init_auth_state()
    session = get_session()
    logged_in = session.get("logged_in", False)
    username = session.get("username")
    role = session.get("role")
    # If not logged in, show limited menu (maybe just login/register links?)
    # But the sidebar is shown on all pages, including login/register.
    # We'll handle that by showing a simplified menu for guests.
    with st.sidebar:
        # ── Logo ─────────────────────────────────────────────────────────
        st.markdown(dedent(f"""
        <div style="padding:1.3rem 1rem 1rem;
            border-bottom:1px solid {COLORS['border_solid']};">
            <div style="display:flex;align-items:center;gap:.7rem;">
                <div style="background:linear-gradient(135deg,{COLORS['primary']},{COLORS['accent']});
                    border-radius:12px;width:40px;height:40px;flex-shrink:0;
                    display:flex;align-items:center;justify-content:center;font-size:1.3rem;">
                    🎓
                </div>
                <div>
                    <div style="color:{COLORS['text']};font-weight:800;font-size:.97rem;"
                        line-height:1.15;">UniQuery</div>
                    <div style="color:{COLORS['muted']};font-size:.68rem;">
                        Query Management System</div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

        if not logged_in:
            # Show only links to login and register for guests
            _section_label("Account")
            st.page_link("pages/Login.py", label="🔐  Login")
            st.page_link("pages/Register.py", label="📝  Register")
        else:
            # Logged-in user menu
            # ── Main nav ──────────────────────────────────────────────────────
            _section_label("Main")
            # Home is always visible
            st.page_link("app.py", label="🏠  Home")
            # Dashboard: only for Admin
            if role == "Admin":
                st.page_link("pages/Dashboard.py", label="📊  Dashboard")
            # Raise Ticket: for Student only
            if role == "Student":
                st.page_link("pages/Raise_Ticket.py", label="🎫  Raise Ticket")
            # Track Ticket: for Student and Faculty
            if role in ("Student", "Faculty"):
                st.page_link("pages/Track_Ticket.py", label="🔍  Track Ticket")
            # Faculty Panel: for Faculty only
            if role == "Faculty":
                st.page_link("pages/Faculty_Panel.py", label="👨‍🏫  Faculty Panel")

            # ── AI Features ───────────────────────────────────────────────────
            _section_label("AI Features")
            # AI Chatbot and Knowledge Base are available to all logged-in users
            st.page_link("pages/AI_Chatbot.py", label="💬  AI Chatbot")
            st.page_link("pages/Knowledge_Base.py", label="📚  Knowledge Base")

            # ── Administration ────────────────────────────────────────────────
            _section_label("Administration")
            # Admin-only section
            if role == "Admin":
                admin_links = [
                    ("pages/Admin_Panel.py", "🛡️  Admin Panel"),
                    ("pages/Analytics.py", "📈  Analytics"),
                    ("pages/Reports.py", "📑  Reports"),
                    ("pages/Notifications.py", "🔔  Notifications"),
                ]
                for path, label in admin_links:
                    try:
                        st.page_link(path, label=label)
                    except Exception:
                        # page file not yet created — render as plain text
                        safe_label = escape(str(label))
                        st.markdown(
                            f'<div style="color:{COLORS["muted"]};font-size:.85rem;"'
                            f'padding:.25rem .6rem;opacity:.5;">{safe_label}</div>',
                            unsafe_allow_html=True,
                        )

            # ── Footer profile ────────────────────────────────────────────────
            # Show user info in the footer
            display_name = username if username else "User"
            display_role = role if role else "Guest"
            # Determine online status indicator color: green for logged in, grey for guest
            status_color = COLORS.get("green", "#22C55E") if logged_in else "#6B7280"
            status_text = "Online" if logged_in else "Offline"
            st.markdown(dedent(f"""
            <div style="position:fixed;bottom:0;left:0;width:260px;
                background:{COLORS['card']};border-top:1px solid {COLORS['border_solid']};
                padding:.75rem 1rem;">
                <div style="display:flex;align-items:center;gap:.6rem;">
                    <div style="background:linear-gradient(135deg,{COLORS['accent']},{COLORS['primary']});
                        border-radius:50%;width:32px;height:32px;flex-shrink:0;
                        display:flex;align-items:center;justify-content:center;font-size:.9rem;">
                        👤
                    </div>
                    <div style="flex:1;min-width:0;">
                        <div style="color:{COLORS['text']};font-size:.82rem;font-weight:600;">
                            {escape(display_name)}
                        </div>
                        <div style="color:{COLORS['muted']};font-size:.7rem;">
                            <span style="display:inline-block;width:6px;height:6px;
                            background:{status_color};border-radius:50%;
                            margin-right:4px;vertical-align:middle;"></span>{status_text}
                            <span style="margin-left:4px;font-size:0.7em;">{escape(display_role)}</span>
                        </div>
                    </div>
                    <span style="color:{COLORS['muted']};font-size:.68rem;">v4.0</span>
                </div>
            </div>
            <div style="height:58px;"></div>
            """), unsafe_allow_html=True)