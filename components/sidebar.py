import streamlit as st
from core.config import THEME


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center;padding:1rem 0 .5rem;">
            <span style="font-size:2.2rem;">🎓</span>
            <div style="color:{THEME['text']};font-weight:700;font-size:1.1rem;margin-top:.3rem;">UniQuery</div>
            <div style="color:{THEME['muted']};font-size:.75rem;">Query Management System</div>
        </div>
        <hr style="border-color:{THEME['border']};margin:.5rem 0 1rem;">
        """, unsafe_allow_html=True)

        st.page_link("app.py",                  label="🏠  Home")
        st.page_link("pages/Dashboard.py",       label="📊  Dashboard")
        st.page_link("pages/Raise_Ticket.py",    label="🎫  Raise Ticket")
        st.page_link("pages/Track_Ticket.py",    label="🔍  Track Ticket")
        st.page_link("pages/Faculty_Panel.py",   label="👨‍🏫  Faculty Panel")

        st.markdown(f"""
        <hr style="border-color:{THEME['border']};margin:1rem 0 .5rem;">
        <div style="color:{THEME['muted']};font-size:.72rem;text-align:center;">v1.0.0 · University QMS</div>
        """, unsafe_allow_html=True)
