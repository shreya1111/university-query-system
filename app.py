import streamlit as st
from core.config import APP_TITLE, APP_ICON, THEME
from core.database import initialize_database
from components.sidebar import render_sidebar

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"],.main{{background:{THEME['bg']}}}
[data-testid="stSidebar"]{{background:#0D1B2E;border-right:1px solid {THEME['border']}}}
section[data-testid="stSidebar"] a{{color:{THEME['muted']}!important}}
section[data-testid="stSidebar"] a:hover{{color:{THEME['text']}!important}}
h1,h2,h3,h4{{color:{THEME['text']}}}
p,li,span,label{{color:{THEME['muted']}}}
.stTextInput>div>div>input,.stTextArea textarea{{
    background:{THEME['secondary_bg']};border-color:{THEME['border']};color:{THEME['text']}}}
div[data-baseweb="select"]>div{{
    background:{THEME['secondary_bg']};border-color:{THEME['border']};color:{THEME['text']}}}
.stButton>button{{
    background:{THEME['primary']};color:#fff;border:none;border-radius:8px;
    padding:.45rem 1.4rem;font-weight:600;transition:opacity .2s}}
.stButton>button:hover{{opacity:.85}}
[data-testid="stMetricLabel"]{{color:{THEME['muted']}!important}}
[data-testid="stMetricValue"]{{color:{THEME['text']}!important}}
hr{{border-color:{THEME['border']}}}
.block-container{{padding:2rem 2rem 1rem}}
</style>
""", unsafe_allow_html=True)

initialize_database()
render_sidebar()

st.markdown(f"""
<div style="text-align:center;padding:3rem 0 1rem;">
    <div style="font-size:4rem;">🎓</div>
    <h1 style="color:{THEME['text']};font-size:2.2rem;margin:.5rem 0 .3rem;">University Query Management System</h1>
    <p style="color:{THEME['muted']};font-size:1rem;">Streamlined query resolution for students and faculty</p>
</div>
<hr style="border-color:{THEME['border']};margin:1rem 0 2rem;">
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div style="background:{THEME['secondary_bg']};border:1px solid {THEME['border']};
    border-radius:10px;padding:1.2rem;text-align:center;">
    <div style="font-size:1.8rem;">📊</div>
    <div style="color:{THEME['text']};font-weight:600;margin:.4rem 0 .2rem;">Dashboard</div>
    <div style="color:{THEME['muted']};font-size:.82rem;">KPIs & analytics</div></div>""",
    unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div style="background:{THEME['secondary_bg']};border:1px solid {THEME['border']};
    border-radius:10px;padding:1.2rem;text-align:center;">
    <div style="font-size:1.8rem;">🎫</div>
    <div style="color:{THEME['text']};font-weight:600;margin:.4rem 0 .2rem;">Raise Ticket</div>
    <div style="color:{THEME['muted']};font-size:.82rem;">Submit a new query</div></div>""",
    unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div style="background:{THEME['secondary_bg']};border:1px solid {THEME['border']};
    border-radius:10px;padding:1.2rem;text-align:center;">
    <div style="font-size:1.8rem;">🔍</div>
    <div style="color:{THEME['text']};font-weight:600;margin:.4rem 0 .2rem;">Track Ticket</div>
    <div style="color:{THEME['muted']};font-size:.82rem;">Filter & search tickets</div></div>""",
    unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div style="background:{THEME['secondary_bg']};border:1px solid {THEME['border']};
    border-radius:10px;padding:1.2rem;text-align:center;">
    <div style="font-size:1.8rem;">👨‍🏫</div>
    <div style="color:{THEME['text']};font-weight:600;margin:.4rem 0 .2rem;">Faculty Panel</div>
    <div style="color:{THEME['muted']};font-size:.82rem;">Manage & resolve queries</div></div>""",
    unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("👈 Use the sidebar to navigate between pages.")
