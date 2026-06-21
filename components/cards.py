import streamlit as st
from core.config import THEME


def kpi_card(label: str, value: int, color: str = THEME["primary"], icon: str = "📌") -> None:
    st.markdown(f"""
    <div style="
        background:{THEME['secondary_bg']};
        border:1px solid {THEME['border']};
        border-left: 4px solid {color};
        border-radius:10px;
        padding:1.2rem 1.4rem;
        text-align:center;
    ">
        <div style="font-size:1.8rem;">{icon}</div>
        <div style="font-size:2rem;font-weight:700;color:{color};line-height:1.2;">{value}</div>
        <div style="color:{THEME['muted']};font-size:.85rem;margin-top:.3rem;">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "") -> None:
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <h1 style="color:{THEME['text']};margin:0;font-size:1.8rem;">{title}</h1>
        {"" if not subtitle else f'<p style="color:{THEME["muted"]};margin:.3rem 0 0;">{subtitle}</p>'}
    </div>
    <hr style="border-color:{THEME['border']};margin-bottom:1.5rem;">
    """, unsafe_allow_html=True)
