import streamlit as st
import pandas as pd
from core.config import APP_ICON, THEME, DEPARTMENTS, PRIORITIES, STATUSES
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from components.ticket_card import ticket_card
from features.ticket_management.service import TicketService

st.set_page_config(page_title="Faculty Panel", page_icon=APP_ICON, layout="wide")
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"],.main{{background:{THEME['bg']}}}
[data-testid="stSidebar"]{{background:#0D1B2E;border-right:1px solid {THEME['border']}}}
h1,h2,h3{{color:{THEME['text']}}} p,span,li,label{{color:{THEME['muted']}}}
.stTextInput>div>div>input,.stTextArea textarea{{
    background:{THEME['secondary_bg']};border-color:{THEME['border']};color:{THEME['text']}}}
div[data-baseweb="select"]>div{{background:{THEME['secondary_bg']};border-color:{THEME['border']};color:{THEME['text']}}}
.stButton>button{{background:#7C3AED;color:#fff;border:none;border-radius:8px;padding:.45rem 1.4rem;font-weight:600}}
.stButton>button:hover{{opacity:.85}}
hr{{border-color:{THEME['border']}}} .block-container{{padding:2rem 2rem 1rem}}
[data-testid="stExpander"]{{background:{THEME['secondary_bg']};border:1px solid {THEME['border']};border-radius:8px}}
</style>""", unsafe_allow_html=True)

initialize_database()
render_sidebar()

# ── Auth ──────────────────────────────────────────────────────────────────────
if "faculty_auth" not in st.session_state:
    st.session_state.faculty_auth = False

if not st.session_state.faculty_auth:
    page_header("👨‍🏫 Faculty Panel", "Restricted access — please log in.")
    _, lc, _ = st.columns([1, 2, 1])
    with lc:
        with st.form("login_form"):
            user = st.text_input("Username")
            pwd  = st.text_input("Password", type="password")
            ok   = st.form_submit_button("🔐 Login", use_container_width=True)
        if ok:
            if user == "faculty" and pwd == "admin123":
                st.session_state.faculty_auth = True
                st.rerun()
            else:
                st.error("Invalid credentials.  (faculty / admin123)")
    st.stop()

# ── Authenticated ─────────────────────────────────────────────────────────────
col_h, col_btn = st.columns([5, 1])
with col_h:
    page_header("👨‍🏫 Faculty Panel", "View, filter, and resolve student queries.")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout"):
        st.session_state.faculty_auth = False
        st.rerun()

svc = TicketService()

fc1, fc2, fc3 = st.columns(3)
with fc1: f_dept   = st.selectbox("Filter Department", ["All"] + DEPARTMENTS)
with fc2: f_pri    = st.selectbox("Filter Priority",   ["All"] + PRIORITIES)
with fc3: f_status = st.selectbox("Filter Status",     ["All"] + STATUSES)

tickets = svc.list_tickets(
    department=None if f_dept   == "All" else f_dept,
    priority  =None if f_pri    == "All" else f_pri,
    status    =None if f_status == "All" else f_status,
)

st.markdown(f"<hr style='border-color:{THEME['border']};'>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{THEME['muted']};'><b style='color:{THEME['text']};'>{len(tickets)}</b> ticket(s)</p>",
            unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🃏 Manage Cards", "📋 Table View"])

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
        df = pd.DataFrame(tickets)[["ticket_id","student_name","department","priority","status","created_at"]]
        df.columns = ["ID","Student","Department","Priority","Status","Created At"]
        st.dataframe(df, use_container_width=True, hide_index=True)
