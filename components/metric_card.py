import streamlit as st
from html import escape
from textwrap import dedent
from styles.theme import COLORS


def metric_card(
    label: str,
    value: int | str,
    icon: str,
    color: str,
    delta: str = "",
    delta_up: bool = True,
) -> None:
    delta_html = ""
    if delta:
        dc = COLORS["green"] if delta_up else COLORS["red"]
        arrow = "\u25b2" if delta_up else "\u25bc"
        delta_html = (f'<div style="color:{dc};font-size:.72rem;'
                      f'font-weight:600;margin-top:.25rem;">{arrow} {escape(str(delta))}</div>')
    safe_label = escape(str(label))
    safe_value = escape(str(value))
    safe_icon  = escape(str(icon))
    card  = COLORS["card"]
    card2 = COLORS["card2"]
    bdr   = COLORS["border"]
    muted = COLORS["muted"]
    st.markdown(
        f'<div style="background:linear-gradient(145deg,{card},{card2});'
        f'border:1px solid {bdr};border-radius:18px;padding:1.3rem 1.1rem;'
        f'position:relative;overflow:hidden;">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
        f'<div>'
        f'<div style="color:{muted};font-size:.7rem;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:.08em;">{safe_label}</div>'
        f'<div style="color:{color};font-size:1.9rem;font-weight:800;'
        f'line-height:1.1;margin-top:.3rem;">{safe_value}</div>'
        f'{delta_html}'
        f'</div>'
        f'<div style="background:{color}22;border:1px solid {color}44;'
        f'border-radius:12px;padding:.55rem;font-size:1.3rem;">{safe_icon}</div>'
        f'</div>'
        f'<div style="position:absolute;bottom:-20px;right:-20px;width:72px;height:72px;'
        f'background:{color}0d;border-radius:50%;"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
