import streamlit as st
from datetime import date
from textwrap import dedent
import os
from core.config import APP_TITLE, APP_ICON
from core.database import initialize_database, get_stats
from components.sidebar import render_sidebar
from components.metric_card import metric_card
from styles.custom_css import inject_css
from styles.theme import COLORS
from features.auth.auth_utils import require_login

# Set page config first
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Check authentication and redirect to login if not logged in
# (allows login and register pages to be accessed without login)
require_login()

# Now we know the user is logged in (or we are on login/register page, but require_login would have redirected)
# Initialize auth state to ensure session variables exist (required for later use)
from features.auth.session import init_auth_state
init_auth_state()

# Get user info for personalized welcome
from features.auth.session import get_session
session = get_session()
username = session.get("username", "User")
role = session.get("role", "Guest")

inject_css()
initialize_database()
render_sidebar()

stats = get_stats()
today = date.today().strftime("%A, %B %d %Y")

# Pre-assign colour tokens to avoid nested-quote breakage inside f-strings
# that use single-quoted HTML attributes (e.g. style='color:...').
_c_text         = COLORS["text"]
_c_muted        = COLORS["muted"]
_c_card         = COLORS["card"]
_c_card2        = COLORS["card2"]
_c_border       = COLORS["border"]
_c_border_solid = COLORS["border_solid"]
_c_primary      = COLORS["primary"]

# ── Welcome banner ────────────────────────────────────────────────────────────
st.markdown(dedent(f"""
<div style="display:flex;justify-content:space-between;align-items:flex-start;
    margin-bottom:1.6rem;flex-wrap:wrap;gap:1rem;">
    <div>
        <h1 style="color:{_c_text};font-size:2rem;font-weight:800;margin:0;">
            Welcome back, {username} 👋
        </h1>
        <p style="color:{_c_muted};margin:.4rem 0 0;font-size:.92rem;">
            Here's what's happening with your queries today.
        </p>
    </div>
    <div style="background:{_c_card};border:1px solid {_c_border_solid};
        border-radius:14px;padding:.65rem 1.1rem;text-align:right;align-self:center;">
        <div style="color:{_c_muted};font-size:.65rem;text-transform:uppercase;
            letter-spacing:.07em;">Today</div>
        <div style="color:{_c_text};font-size:.88rem;font-weight:600;">{today}</div>
    </div>
</div>
<div style="height:1px;background:linear-gradient(90deg,{_c_primary}88,transparent);
    margin-bottom:1.8rem;"></div>
"""), unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1: metric_card("Total Tickets",   stats["total"],       "🎫", COLORS["primary"])
with k2: metric_card("Pending",         stats["pending"],     "⏳", COLORS["orange"])
with k3: metric_card("In Progress",     stats["in_progress"], "🔄", COLORS["blue"])
with k4: metric_card("Resolved",        stats["resolved"],    "✅", COLORS["green"])

st.markdown("<div style='height:1.6rem;'></div>", unsafe_allow_html=True)

# ── Navigation cards (clickable via st.switch_page) ───────────────────────────
st.markdown(
    f"<h2 style='color:{_c_text};font-size:1.05rem;font-weight:700;"
    f"margin-bottom:1rem;'>🚀 Quick Navigation</h2>",
    unsafe_allow_html=True,
)

NAV = [
    ("pages/Dashboard.py",     "📊", "Dashboard",      "KPIs & real-time analytics",       COLORS["primary"]),
    ("pages/Raise_Ticket.py",  "🎫", "Raise Ticket",   "Submit a new student query",       COLORS["accent"]),
    ("pages/Track_Ticket.py",  "🔍", "Track Ticket",   "Filter & search all tickets",      COLORS["blue"]),
    ("pages/Faculty_Panel.py", "👨‍🏫", "Faculty Panel", "Manage & resolve queries",         COLORS["cyan"]),
    ("pages/AI_Chatbot.py",    "💬", "AI Chatbot",     "Instant policy Q&A via RAG",       COLORS["green"]),
    ("pages/Knowledge_Base.py","📚", "Knowledge Base", "Search university documents",      COLORS["orange"]),
]

rows = [NAV[:3], NAV[3:]]
for row in rows:
    cols = st.columns(3)
    for col, (page, icon, label, desc, color) in zip(cols, row):
        with col:
            # The card IS the visual header; the single button below is the
            # call-to-action. One consistent element — no separate decorative
            # div plus a redundant "Open X" button.
            st.markdown(dedent(f"""
            <div style="background:linear-gradient(145deg,{_c_card},{_c_card2});
                border:1px solid {_c_border};border-radius:18px;padding:1.3rem;
                text-align:center;margin-bottom:.6rem;">
                <div style="background:{color}22;border:1px solid {color}44;border-radius:12px;
                    width:46px;height:46px;display:flex;align-items:center;justify-content:center;
                    font-size:1.4rem;margin:0 auto .7rem;">{icon}</div>
                <div style="color:{_c_text};font-weight:700;font-size:.92rem;
                    margin-bottom:.2rem;">{label}</div>
                <div style="color:{_c_muted};font-size:.75rem;">{desc}</div>
            </div>"""), unsafe_allow_html=True)
            if st.button(label, key=f"nav_{label}", use_container_width=True):
                st.switch_page(page)
    st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)