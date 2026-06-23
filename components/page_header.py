import streamlit as st
from html import escape
from textwrap import dedent
from styles.theme import COLORS


def page_header(title: str, subtitle: str = "") -> None:
    """Render a page header with title and optional subtitle."""
    safe_title = escape(str(title))
    safe_subtitle = escape(str(subtitle)).replace("\n", "<br>") if subtitle else ""
    sub_html = (
        f'<p style="color:{COLORS["muted"]};margin:0.5rem 0 0;font-size:1.1rem;font-weight:400;">'
        f'{safe_subtitle}</p>'
    ) if subtitle else ""
    st.markdown(
        f'<div style="margin-bottom:1.5rem;">'
        f'<h1 style="color:{COLORS["text"]};margin:0;font-size:2.2rem;font-weight:800;letter-spacing:-0.5px;">{safe_title}</h1>'
        f'{sub_html}'
        f'</div>',
        unsafe_allow_html=True,
    )