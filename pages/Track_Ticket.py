import streamlit as st
import pandas as pd
from core.config import APP_ICON, THEME, DEPARTMENTS, PRIORITIES, STATUSES
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from components.ticket_card import ticket_card
from features.ticket_management.service import TicketService

st.set_page_config(page_title="Track Ticket", page_icon=APP_ICON, layout="wide")
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"],.main{{background:{THEME['bg']}}}
[data-testid="stSidebar"]{{background:#0D1B2E;border-right:1px solid {THEME['border']}}}
h1,h2,h3{{color:{THEME['text']}}} p,span,li,label{{color:{THEME['muted']}}}
.stTextInput>div>div>input{{background:{THEME['secondary_bg']};border-color:{THEME['border']};color:{THEME['text']}}}
div[data-baseweb="select"]>div{{background:{THEME['secondary_bg']};border-color:{THEME['border']};color:{THEME['text']}}}
.stButton>button{{background:{THEME['primary']};color:#fff;border:none;border-radius:8px;padding:.45rem 1.4rem;font-weight:600}}
hr{{border-color:{THEME['border']}}} .block-container{{padding:2rem 2rem 1rem}}
</style>""", unsafe_allow_html=True)

initialize_database()
render_sidebar()
page_header("🔍 Track Tickets", "Filter and search all submitted queries.")

svc = TicketService()

# Filters
fc1, fc2, fc3 = st.columns(3)
with fc1: f_dept   = st.selectbox("Department",  ["All"] + DEPARTMENTS)
with fc2: f_pri    = st.selectbox("Priority",    ["All"] + PRIORITIES)
with fc3: f_status = st.selectbox("Status",      ["All"] + STATUSES)

tickets = svc.list_tickets(
    department=None if f_dept   == "All" else f_dept,
    priority  =None if f_pri    == "All" else f_pri,
    status    =None if f_status == "All" else f_status,
)

st.markdown(f"<hr style='border-color:{THEME['border']};'>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🃏 Card View", "📋 Table View"])

with tab1:
    if not tickets:
        st.info("No tickets match the selected filters.")
    else:
        st.markdown(f"<p style='color:{THEME['muted']};margin-bottom:.8rem;'><b style='color:{THEME['text']};'>{len(tickets)}</b> ticket(s) found</p>",
                    unsafe_allow_html=True)
        for t in tickets:
            ticket_card(t)

with tab2:
    if not tickets:
        st.info("No tickets match the selected filters.")
    else:
        df = pd.DataFrame(tickets)[["ticket_id","student_name","department","priority","status","created_at"]]
        df.columns = ["ID","Student","Department","Priority","Status","Created At"]
        st.dataframe(df, use_container_width=True, hide_index=True)
