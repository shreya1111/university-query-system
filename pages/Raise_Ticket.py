import streamlit as st
from core.config import APP_ICON, THEME, DEPARTMENTS, PRIORITIES
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from features.ticket_management.service import TicketService

st.set_page_config(page_title="Raise Ticket", page_icon=APP_ICON, layout="wide")
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"],.main{{background:{THEME['bg']}}}
[data-testid="stSidebar"]{{background:#0D1B2E;border-right:1px solid {THEME['border']}}}
h1,h2,h3{{color:{THEME['text']}}} p,span,li,label{{color:{THEME['muted']}}}
.stTextInput>div>div>input,.stTextArea textarea{{
    background:{THEME['secondary_bg']};border-color:{THEME['border']};color:{THEME['text']}}}
div[data-baseweb="select"]>div{{
    background:{THEME['secondary_bg']};border-color:{THEME['border']};color:{THEME['text']}}}
.stButton>button{{background:{THEME['primary']};color:#fff;border:none;border-radius:8px;
    padding:.45rem 1.4rem;font-weight:600}}
.stButton>button:hover{{opacity:.85}}
hr{{border-color:{THEME['border']}}} .block-container{{padding:2rem 2rem 1rem}}
</style>""", unsafe_allow_html=True)

initialize_database()
render_sidebar()
page_header("🎫 Raise a New Ticket", "Submit your query and we'll get back to you shortly.")

_, form_col, _ = st.columns([1, 3, 1])
with form_col:
    with st.form("raise_form", clear_on_submit=True):
        student_name = st.text_input("Student Name *")
        col1, col2 = st.columns(2)
        with col1:
            department = st.selectbox("Department *", DEPARTMENTS)
        with col2:
            priority = st.selectbox("Priority *", PRIORITIES)
        query = st.text_area("Query *", height=140,
                             placeholder="Describe your issue in detail…")
        submitted = st.form_submit_button("🚀 Submit Ticket", use_container_width=True)

    if submitted:
        errors = []
        if not student_name.strip(): errors.append("Student Name is required.")
        if not query.strip():        errors.append("Query description is required.")
        if errors:
            for e in errors: st.error(e)
        else:
            svc = TicketService()
            tid = svc.raise_ticket(student_name.strip(), query.strip(), department, priority)
            st.success(f"✅ Ticket #{tid} submitted successfully!")
            st.markdown(f"""
            <div style="background:{THEME['secondary_bg']};border:1px solid {THEME['success']};
            border-radius:10px;padding:1rem 1.2rem;margin-top:.5rem;">
                <div style="color:{THEME['success']};font-weight:700;font-size:1rem;">🎫 Ticket ID: #{tid}</div>
                <div style="color:{THEME['muted']};font-size:.85rem;margin-top:.3rem;">
                    Use this ID on the <strong>Track Ticket</strong> page to follow up.
                </div>
            </div>""", unsafe_allow_html=True)
