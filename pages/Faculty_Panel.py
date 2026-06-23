import streamlit as st
import pandas as pd
from textwrap import dedent
from core.config import APP_ICON, DEPARTMENTS, PRIORITIES, STATUSES
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from components.ticket_card import ticket_card
from styles.custom_css import inject_css
from styles.theme import COLORS
from features.ticket_management.service import TicketService
from features.auth.auth_utils import require_login
from features.auth.session import get_session

st.set_page_config(page_title="Faculty Panel", page_icon=APP_ICON, layout="wide")
require_login()
# Check if the user is faculty
session = get_session()
if session.get("role") != "Faculty":
    st.error("Access denied: This page is for faculty only.")
    st.stop()

inject_css()
initialize_database()
render_sidebar()

# Pre-assign tokens
_c_text  = COLORS["text"]
_c_muted = COLORS["muted"]
_c_card  = COLORS["card"]
_c_card2 = COLORS["card2"]
_c_border = COLORS["border"]

svc = TicketService()

col_h, col_btn = st.columns([5, 1])
with col_h:
    page_header("👨‍🏫 Faculty Panel", "View, filter, and resolve student queries.")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout"):
        from features.auth.service import logout_user
        logout_user()
        st.rerun()

st.markdown(dedent(f"""
<div style="background:linear-gradient(145deg,{_c_card},{_c_card2});
    border:1px solid {_c_border};border-radius:16px;
    padding:1.2rem;margin-bottom:1rem;">
"""), unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns(3)
with fc1: f_dept   = st.selectbox("Filter Department", ["All"] + DEPARTMENTS)
with fc2: f_pri    = st.selectbox("Filter Priority",   ["All"] + PRIORITIES)
with fc3: f_status = st.selectbox("Filter Status",     ["All"] + STATUSES)
st.markdown("</div>", unsafe_allow_html=True)

tickets = svc.list_tickets(
    department=None if f_dept   == "All" else f_dept,
    priority  =None if f_pri    == "All" else f_pri,
    status    =None if f_status == "All" else f_status,
)

st.markdown(
    f"<p style='color:{_c_muted};font-size:.84rem;margin:.2rem 0 .8rem;'>"
    f"<b style='color:{_c_text};'>{len(tickets)}</b> ticket(s)</p>",
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["🃏  Manage Cards", "📋  Table View"])

with tab1:
    if not tickets:
        st.info("No tickets match the selected filters.")
    else:
        for t in tickets:
            ticket_card(t, show_actions=True, service=svc)

with tab2:
    if not tickets:
        st.info("No tickets match the selected filters.")
    else:
        df = pd.DataFrame(tickets)
        cols = [c for c in ["ticket_id", "student_name", "department", "priority", "status",
                             "intent", "sentiment", "summary", "created_at"] if c in df.columns]
        df = df[cols]
        df.columns = [c.replace("_", " ").title() for c in cols]
        st.dataframe(df, use_container_width=True, hide_index=True)