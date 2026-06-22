import streamlit as st
from html import escape
from styles.theme import COLORS


def notification_item(
    message: str,
    timestamp: str,
    icon: str = "🔔",
    color: str = COLORS["primary"],
    unread: bool = True,
) -> None:
    dot = (
        f'<span style="display:inline-block;width:7px;height:7px;'
        f'background:{COLORS["green"]};border-radius:50%;margin-left:6px;'
        f'vertical-align:middle;"></span>'
        if unread else ""
    )
    st.markdown(f"""
<div style="display:flex;gap:.8rem;align-items:flex-start;
    padding:.65rem .4rem;border-bottom:1px solid {COLORS['border_solid']};">
    <div style="background:{color}22;border:1px solid {color}44;border-radius:50%;
        width:34px;height:34px;flex-shrink:0;
        display:flex;align-items:center;justify-content:center;font-size:1rem;">
        {icon}
    </div>
    <div style="flex:1;min-width:0;">
        <div style="color:{COLORS['text']};font-size:.84rem;line-height:1.4;">
            {escape(str(message))}{dot}
        </div>
        <div style="color:{COLORS['muted']};font-size:.72rem;margin-top:.2rem;">
            {escape(str(timestamp)[:16])}
        </div>
    </div>
</div>""", unsafe_allow_html=True)