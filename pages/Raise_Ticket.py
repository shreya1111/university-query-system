import re
import streamlit as st
from html import escape
from core.config import APP_ICON
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from styles.custom_css import inject_css
from styles.theme import COLORS, PRIORITY_COLORS, SENTIMENT_COLORS
from features.ticket_management.service import TicketService
from features.auth.auth_utils import require_login

st.set_page_config(page_title="Raise Ticket", page_icon=APP_ICON, layout="wide")
require_login()
inject_css()
initialize_database()
render_sidebar()
page_header("🎫 Raise a New Ticket",
            "Submit your query — AI will analyse and route it automatically.")

# Pre-assign tokens
_c_text   = COLORS["text"]
_c_muted  = COLORS["muted"]
_c_card   = COLORS["card"]
_c_card2  = COLORS["card2"]
_c_border = COLORS["border"]
_c_bs     = COLORS["border_solid"]
_c_bg     = COLORS["bg"]
_c_accent = COLORS["accent"]
_c_green  = COLORS["green"]

_, form_col, _ = st.columns([1, 3, 1])
with form_col:
    st.markdown(f"""
    <div style="background:linear-gradient(145deg,{_c_card},{_c_card2});
        border:1px solid {_c_border};border-radius:20px;padding:2rem;
        margin-bottom:1rem;">
    """, unsafe_allow_html=True)

    with st.form("raise_form", clear_on_submit=True):
        student_name = st.text_input("👤 Student Name *",
                                     placeholder="e.g. Riya Sharma")
        query_input = st.text_area("📝 Describe your query *", height=140,
                                   placeholder="e.g. My admit card has not been "
                                               "generated and exams are tomorrow.")
        submitted = st.form_submit_button("🚀  Submit & Analyse with AI",
                                          use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        name_clean  = re.sub(r"<[^>]+>", "", student_name).strip()
        query_clean = re.sub(r"<[^>]+>", "", query_input).strip()

        if not name_clean:
            st.error("Student Name is required.")
        elif not query_clean:
            st.error("Query description is required.")
        else:
            with st.spinner("🤖 AI is analysing your query…"):
                svc = TicketService()
                tid, ai = svc.raise_ticket_with_ai(name_clean, query_clean)

            st.success(f"✅ Ticket #{tid} submitted and analysed!")
            st.markdown("<div style='height:.6rem;'></div>", unsafe_allow_html=True)

            pri_color = PRIORITY_COLORS.get(ai["priority"], COLORS["muted"])
            sen_color = SENTIMENT_COLORS.get(ai["sentiment"], COLORS["muted"])

            # FIX: was COLORS['text'] inside single-quoted outer string → raw HTML
            st.markdown(
                f"<div style='color:{_c_text};font-weight:700;"
                f"font-size:.95rem;margin-bottom:.7rem;'>🤖 AI Intelligence Report</div>",
                unsafe_allow_html=True,
            )

            c1, c2, c3 = st.columns(3)
            for col, lbl, val, color, icn in [
                (c1, "Detected Intent",  ai["intent"],     COLORS["primary"], "🎯"),
                (c2, "Routed To",        ai["department"], COLORS["cyan"],    "🏢"),
                (c3, "AI Priority",      ai["priority"],   pri_color,         "⚡"),
            ]:
                with col:
                    st.markdown(f"""
    <div style="background:{_c_card2};border:1px solid {_c_border};
        border-left:3px solid {color};border-radius:14px;padding:1rem;">
        <div style="color:{_c_muted};font-size:.68rem;font-weight:700;
            text-transform:uppercase;letter-spacing:.08em;">{icn} {escape(lbl)}</div>
        <div style="color:{color};font-weight:700;font-size:.97rem;
            margin-top:.3rem;">{escape(str(val))}</div>
    </div>""", unsafe_allow_html=True)

            st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
            c4, c5 = st.columns(2)
            with c4:
                st.markdown(f"""
    <div style="background:{_c_card2};border:1px solid {_c_border};
        border-left:3px solid {_c_accent};border-radius:14px;padding:1rem;">
        <div style="color:{_c_muted};font-size:.68rem;font-weight:700;
            text-transform:uppercase;letter-spacing:.08em;">📝 Summary</div>
        <div style="color:{_c_text};font-size:.9rem;margin-top:.3rem;">
            {escape(str(ai['summary']))}</div>
    </div>""", unsafe_allow_html=True)
            with c5:
                st.markdown(f"""
    <div style="background:{_c_card2};border:1px solid {_c_border};
        border-left:3px solid {sen_color};border-radius:14px;padding:1rem;">
        <div style="color:{_c_muted};font-size:.68rem;font-weight:700;
            text-transform:uppercase;letter-spacing:.08em;">💬 Sentiment</div>
        <div style="color:{sen_color};font-weight:700;font-size:.97rem;
            margin-top:.3rem;">{escape(str(ai['sentiment']))}</div>
    </div>""", unsafe_allow_html=True)

            st.mark("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
            with st.expander("💬 Auto-generated Reply", expanded=True):
                st.markdown(f"""
    <div style="background:{_c_bg};border-radius:10px;padding:.9rem 1.1rem;
        color:{_c_text};font-size:.9rem;line-height:1.7;
        border:1px solid {_c_bs};">
        {escape(str(ai['auto_reply'])).replace(chr(10), '<br>')}
    </div>""", unsafe_allow_html=True)

            st.markdown(f"""
    <div style="background:{_c_card};border:1px solid {_c_green}55;
        border-left:3px solid {_c_green};border-radius:12px;
        padding:.8rem 1.2rem;margin-top:.8rem;">
        <span style="color:{_c_green};font-weight:700;">🎫 Ticket ID: #{tid}</span>
        <span style="color:{_c_muted};font-size:.85rem;margin-left:1rem;">
            Use this on the Track Ticket page to follow up.</span>
    </div>""", unsafe_allow_html=True)