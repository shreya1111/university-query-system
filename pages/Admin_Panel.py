import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.config import APP_ICON
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from components.metric_card import metric_card
from components.notification_card import notification_item
from styles.custom_css import inject_css
from styles.theme import COLORS, CHART_COLORS, PRIORITY_COLORS, STATUS_COLORS
from features.analytics.ticket_analytics import (
    get_total_tickets, get_pending_tickets, get_in_progress_tickets,
    get_resolved_tickets, get_high_priority_tickets, get_all_tickets_raw,
)
from features.analytics.department_analytics import (
    department_performance, most_active_department, department_ticket_counts,
)
from features.analytics.resolution_analytics import (
    resolution_summary, fastest_department, slowest_department,
)
from features.analytics.satisfaction_analytics import (
    average_satisfaction_score, top_issues,
)
from features.analytics.notifications.notification_service import (
    get_notifications, unread_count,
)

st.set_page_config(page_title="Admin Panel", page_icon="🛡️", layout="wide")
inject_css()
initialize_database()
render_sidebar()
page_header("🛡️ Admin Panel", "System-wide oversight, KPIs, and operational intelligence.")

# Pre-assign tokens to avoid nested-quote breakage
_c_text  = COLORS["text"]
_c_muted = COLORS["muted"]


def _dark_layout(fig: go.Figure, height: int = 280) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["muted"], family="Inter"),
        margin=dict(t=20, b=10, l=10, r=10), height=height,
        legend=dict(font=dict(color=COLORS["muted"], size=10), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor=COLORS["border_solid"], color=COLORS["muted"]),
        yaxis=dict(gridcolor=COLORS["border_solid"], color=COLORS["muted"]),
    )
    return fig


def _info_card(label: str, value: str, color: str) -> None:
    st.markdown(f"""
    <div style="background:{COLORS['card2']};border:1px solid {COLORS['border']};
        border-left:3px solid {color};border-radius:12px;
        padding:.75rem 1rem;margin-bottom:.5rem;">
        <div style="color:{COLORS['muted']};font-size:.68rem;font-weight:700;
            text-transform:uppercase;letter-spacing:.07em;">{label}</div>
        <div style="color:{color};font-weight:700;font-size:.97rem;
            margin-top:.2rem;">{value}</div>
    </div>""", unsafe_allow_html=True)


# ── KPI row ───────────────────────────────────────────────────────────────────
res     = resolution_summary()
sat     = average_satisfaction_score()
sat_pct = f"{sat}/5.0"

k1, k2, k3, k4 = st.columns(4)
with k1: metric_card("Total Tickets",   get_total_tickets(),       "🎫", COLORS["primary"])
with k2: metric_card("Pending",         get_pending_tickets(),     "⏳", COLORS["orange"])
with k3: metric_card("In Progress",     get_in_progress_tickets(), "🔄", COLORS["blue"])
with k4: metric_card("Resolved",        get_resolved_tickets(),    "✅", COLORS["green"])

st.markdown("<div style='height:.8rem;'></div>", unsafe_allow_html=True)

k5, k6, k7, k8 = st.columns(4)
with k5: metric_card("High Priority",      get_high_priority_tickets(),        "🔴", COLORS["red"])
with k6: metric_card("Resolution Rate",    f"{res['resolution_rate']}%",       "📈", COLORS["cyan"])
with k7: metric_card("Avg Days Open",      f"{res['avg_days_open']}d",         "📅", COLORS["orange"])
with k8: metric_card("Satisfaction Score", sat_pct,                             "⭐", COLORS["green"])

st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

# ── Row 2: Charts + Quick Stats ───────────────────────────────────────────────
ch_left, ch_mid, ch_right = st.columns([2, 2, 1])

with ch_left:
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;"
        f"margin-bottom:.4rem;'>🏢 Department Ticket Distribution</div>",
        unsafe_allow_html=True,
    )
    dept_counts = department_ticket_counts()
    if dept_counts:
        fig_pie = go.Figure(go.Pie(
            labels=[d["department"] for d in dept_counts],
            values=[d["count"] for d in dept_counts],
            hole=.48,
            marker=dict(colors=CHART_COLORS, line=dict(color=COLORS["bg"], width=2)),
            textfont=dict(color="white", size=10),
        ))
        st.plotly_chart(_dark_layout(fig_pie, 280), use_container_width=True)
    else:
        st.info("No data yet.")

with ch_mid:
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;"
        f"margin-bottom:.4rem;'>🔥 Top Issue Categories</div>",
        unsafe_allow_html=True,
    )
    issues = top_issues()
    if issues:
        fig_bar = go.Figure(go.Bar(
            x=[i["count"] for i in issues],
            y=[i["intent"] for i in issues],
            orientation="h",
            marker_color=CHART_COLORS[:len(issues)],
            text=[i["count"] for i in issues],
            textposition="outside",
            textfont=dict(color="white", size=11),
        ))
        st.plotly_chart(_dark_layout(fig_bar, 280), use_container_width=True)
    else:
        st.info("No intent data yet.")

with ch_right:
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;"
        f"margin-bottom:.7rem;'>⚡ Quick Stats</div>",
        unsafe_allow_html=True,
    )
    _info_card("Most Active Dept",   most_active_department(),  COLORS["primary"])
    _info_card("Fastest Resolution", fastest_department(),      COLORS["green"])
    _info_card("Needs Attention",    slowest_department(),      COLORS["red"])
    _info_card("Notifications",      str(unread_count()),       COLORS["orange"])

st.markdown("<hr>", unsafe_allow_html=True)

# ── Row 3: Recent tickets + notifications ─────────────────────────────────────
tbl_col, notif_col = st.columns([3, 2])

with tbl_col:
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;"
        f"margin-bottom:.6rem;'>🕐 Recent Ticket Activity</div>",
        unsafe_allow_html=True,
    )
    tickets = get_all_tickets_raw()[:10]
    if tickets:
        df = pd.DataFrame(tickets)
        show = [c for c in ["ticket_id", "student_name", "department", "priority", "status", "created_at"]
                if c in df.columns]
        df = df[show]
        df.columns = [c.replace("_", " ").title() for c in show]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No tickets yet.")

with notif_col:
    n_count = unread_count()
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;"
        f"margin-bottom:.6rem;'>🔔 Recent Notifications "
        f"<span style='color:{COLORS['orange']};font-size:.78rem;'>"
        f"({n_count})</span></div>",
        unsafe_allow_html=True,
    )
    notifs = get_notifications(8)
    if notifs:
        for n in notifs:
            notification_item(n["message"], n.get("timestamp", ""),
                              icon="🔔", color=COLORS["primary"])
    else:
        st.info("No notifications yet.")

# ── Row 4: Department performance table ──────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;"
    f"margin-bottom:.6rem;'>📊 Department Performance Breakdown</div>",
    unsafe_allow_html=True,
)
dp = department_performance()
if dp:
    df_d = pd.DataFrame(dp)
    df_d.columns = [c.replace("_", " ").title() for c in df_d.columns]
    st.dataframe(df_d, use_container_width=True, hide_index=True)
else:
    st.info("No department data yet.")