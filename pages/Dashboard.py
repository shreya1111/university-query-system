import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from textwrap import dedent
from core.config import APP_ICON
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from components.metric_card import metric_card
from features.ticket_management.service import TicketService
from styles.custom_css import inject_css
from styles.theme import COLORS, CHART_COLORS, PRIORITY_COLORS

st.set_page_config(page_title="Dashboard", page_icon=APP_ICON, layout="wide")
inject_css()
initialize_database()
render_sidebar()

svc       = TicketService()
stats     = svc.dashboard_stats()
dept_data = svc.dept_chart_data()
pri_data  = svc.priority_chart_data()

page_header("📊 Dashboard", "Real-time overview of all university queries")

# Pre-assign tokens to avoid nested-quote breakage in single-quoted HTML attrs
_c_text    = COLORS["text"]
_c_muted   = COLORS["muted"]
_c_card    = COLORS["card"]
_c_card2   = COLORS["card2"]
_c_border  = COLORS["border"]
_c_primary = COLORS["primary"]
_c_bg      = COLORS["bg"]
_c_bs      = COLORS["border_solid"]

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1: metric_card("Total Tickets",   stats["total"],       "🎫", COLORS["primary"])
with k2: metric_card("Pending",         stats["pending"],     "⏳", COLORS["orange"])
with k3: metric_card("In Progress",     stats["in_progress"], "🔄", COLORS["blue"])
with k4: metric_card("Resolved",        stats["resolved"],    "✅", COLORS["green"])

st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
cl, cr = st.columns(2)

with cl:
    st.markdown(
        f"<div style='color:{_c_text};font-size:.92rem;font-weight:700;"
        f"margin-bottom:.5rem;'>🏢 Department Distribution</div>",
        unsafe_allow_html=True,
    )
    if dept_data:
        fig = go.Figure(go.Pie(
            labels=[d["department"] for d in dept_data],
            values=[d["count"] for d in dept_data],
            hole=.5,
            marker=dict(colors=CHART_COLORS, line=dict(color=_c_bg, width=2)),
            textfont=dict(color="white", size=11),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=_c_muted, family="Inter"),
            margin=dict(t=10, b=10, l=10, r=10), height=300,
            legend=dict(font=dict(color=_c_muted, size=10), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data yet.")

with cr:
    st.markdown(
        f"<div style='color:{_c_text};font-size:.92rem;font-weight:700;"
        f"margin-bottom:.5rem;'>⚡ Priority Breakdown</div>",
        unsafe_allow_html=True,
    )
    if pri_data:
        labels = [d["priority"] for d in pri_data]
        values = [d["count"]    for d in pri_data]
        fig2 = go.Figure(go.Bar(
            x=labels, y=values,
            marker_color=[PRIORITY_COLORS.get(p, _c_primary) for p in labels],
            text=values, textposition="outside",
            textfont=dict(color="white", size=12),
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=_c_muted, family="Inter"),
            xaxis=dict(color=_c_muted, gridcolor="rgba(0,0,0,0)"),
            yaxis=dict(color=_c_muted, gridcolor=_c_bs),
            margin=dict(t=30, b=0, l=0, r=0), height=300, bargap=0.4,
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data yet.")

# ── Recent tickets ────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    f"<div style='color:{_c_text};font-size:.92rem;font-weight:700;"
    f"margin-bottom:.8rem;'>🕐 Recent Tickets</div>",
    unsafe_allow_html=True,
)
recent = svc.list_tickets()[:10]
if recent:
    df = pd.DataFrame(recent)
    show = [c for c in ["ticket_id", "student_name", "department", "priority", "status", "created_at"]
            if c in df.columns]
    df = df[show]
    df.columns = [c.replace("_", " ").title() for c in show]
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No tickets yet. Raise one to get started!")