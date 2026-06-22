import streamlit as st
from html import escape
from textwrap import dedent
from styles.theme import COLORS


def _section_label(text: str) -> None:
    safe_text = escape(str(text))
    st.markdown(
        f'<div style="color:{COLORS["muted"]};font-size:.68rem;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:.1em;'
        f'padding:.9rem 1rem .25rem;margin:0;">{safe_text}</div>',
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
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
                    <div style="color:{COLORS['text']};font-weight:800;font-size:.97rem;
                        line-height:1.15;">UniQuery</div>
                    <div style="color:{COLORS['muted']};font-size:.68rem;">
                        Query Management System</div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

        # ── Main nav ──────────────────────────────────────────────────────
        _section_label("Main")
        st.page_link("app.py",                   label="🏠  Home")
        st.page_link("pages/Dashboard.py",        label="📊  Dashboard")
        st.page_link("pages/Raise_Ticket.py",     label="🎫  Raise Ticket")
        st.page_link("pages/Track_Ticket.py",     label="🔍  Track Ticket")
        st.page_link("pages/Faculty_Panel.py",    label="👨‍🏫  Faculty Panel")

        # ── AI Features ───────────────────────────────────────────────────
        _section_label("AI Features")
        st.page_link("pages/AI_Chatbot.py",       label="💬  AI Chatbot")
        st.page_link("pages/Knowledge_Base.py",   label="📚  Knowledge Base")

        # ── Administration ────────────────────────────────────────────────
        _section_label("Administration")
        for path, label in [
            ("pages/Admin_Panel.py",   "🛡️  Admin Panel"),
            ("pages/Analytics.py",     "📈  Analytics"),
            ("pages/Reports.py",       "📑  Reports"),
            ("pages/Notifications.py", "🔔  Notifications"),
        ]:
            try:
                st.page_link(path, label=label)
            except Exception:
                # page file not yet created — render as plain text
                safe_label = escape(str(label))
                st.markdown(
                    f'<div style="color:{COLORS["muted"]};font-size:.85rem;'
                    f'padding:.25rem .6rem;opacity:.5;">{safe_label}</div>',
                    unsafe_allow_html=True,
                )

        # ── Footer profile ────────────────────────────────────────────────
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
                        Admin</div>
                    <div style="color:{COLORS['muted']};font-size:.7rem;">
                        <span style="display:inline-block;width:6px;height:6px;
                        background:{COLORS['green']};border-radius:50%;
                        margin-right:4px;vertical-align:middle;"></span>Online
                    </div>
                </div>
                <span style="color:{COLORS['muted']};font-size:.68rem;">v4.0</span>
            </div>
        </div>
        <div style="height:58px;"></div>
        """), unsafe_allow_html=True)