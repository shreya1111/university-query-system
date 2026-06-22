import streamlit as st
from html import escape
from textwrap import dedent
from styles.theme import COLORS


def kpi_card(label: str, value: int, color: str = COLORS["primary"], icon: str = "📌") -> None:
    safe_label = escape(str(label))
    safe_value = escape(str(value))
    safe_icon = escape(str(icon))
    st.markdown(dedent(f"""
    <div style="background:linear-gradient(145deg,{COLORS['card']},{COLORS['card2']});
        border:1px solid {COLORS['border']};border-radius:18px;padding:1.3rem 1.1rem;
        position:relative;overflow:hidden;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
                <div style="color:{COLORS['muted']};font-size:.7rem;font-weight:700;
                    text-transform:uppercase;letter-spacing:.08em;">{safe_label}</div>
                <div style="color:{color};font-size:1.9rem;font-weight:800;
                    line-height:1.1;margin-top:.3rem;">{safe_value}</div>
            </div>
            <div style="background:{color}22;border:1px solid {color}44;
                border-radius:12px;padding:.55rem;font-size:1.3rem;">{safe_icon}</div>
        </div>
        <div style="position:absolute;bottom:-20px;right:-20px;width:72px;height:72px;
            background:{color}0d;border-radius:50%;"></div>
    </div>"""), unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "") -> None:
    safe_title = escape(str(title))
    safe_subtitle = escape(str(subtitle)).replace("\n", "<br>")
    sub = (f'<p style="color:{COLORS["muted"]};margin:.3rem 0 0;font-size:.88rem;">'
           f'{safe_subtitle}</p>') if subtitle else ""
    st.markdown(dedent(f"""
    <div style="margin-bottom:1.2rem;">
        <h1 style="color:{COLORS['text']};margin:0;font-size:1.65rem;font-weight:800;">
            {safe_title}</h1>
        {sub}
    </div>
    <div style="height:1px;background:linear-gradient(90deg,{COLORS['primary']}88,transparent);
        margin-bottom:1.4rem;"></div>
    """), unsafe_allow_html=True)