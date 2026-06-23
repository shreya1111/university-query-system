import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from core.config import APP_ICON
from core.database import (
    initialize_database,
    get_dept_distribution,
    get_all_tickets,
)
from components.sidebar import render_sidebar
from components.cards import page_header
from components.metric_card import metric_card
from styles.custom_css import inject_css
from styles.theme import COLORS, CHART_COLORS, PRIORITY_COLORS, STATUS_COLORS, SENTIMENT_COLORS


def _rgba(hex_color: str, alpha: float) -> str:
    """Convert '#RRGGBB' hex to 'rgba(r,g,b,a)' for Plotly compatibility."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")
inject_css()
initialize_database()
render_sidebar()
page_header("📈 Analytics", "Interactive charts and deep-dive insights.")

# Pre-assign token to avoid nested-quote breakage
_c_text  = COLORS["text"]
_c_muted = COLORS["muted"]


def _dl(fig: go.Figure, height: int = 300) -> go.Figure:
    """Apply consistent dark layout to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=_c_muted, family="Inter"),
        margin=dict(t=28, b=10, l=10, r=10), height=height,
        legend=dict(font=dict(color=_c_muted, size=10), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor=COLORS["border_solid"], color=_c_muted),
        yaxis=dict(gridcolor=COLORS["border_solid"], color=_c_muted),
    )
    return fig


def _wrap(title: str, subtitle: str = "") -> None:
    # FIX: was using COLORS['text'] inside a single-quoted outer f-string → broken HTML
    sub = (
        f'<span style="color:{_c_muted};font-size:.75rem;margin-left:.5rem;">{subtitle}</span>'
        if subtitle else ""
    )
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;"
        f"margin-bottom:.3rem;'>{title}{sub}</div>",
        unsafe_allow_html=True,
    )


# Helper functions to compute analytics from ticket list
def compute_department_distribution(tickets: List[Dict]) -> List[Dict[str, Any]]:
    if not tickets:
        return []
    dept_count = {}
    for t in tickets:
        dept = t.get("department", "Unknown")
        dept_count[dept] = dept_count.get(dept, 0) + 1
    return [{"department": dept, "count": count} for dept, count in dept_count.items()]


def compute_priority_distribution(tickets: List[Dict]) -> List[Dict[str, Any]]:
    if not tickets:
        return []
    pri_count = {}
    for t in tickets:
        pri = t.get("priority", "Unknown")
        pri_count[pri] = pri_count.get(pri, 0) + 1
    return [{"priority": pri, "count": count} for pri, count in pri_count.items()]


def compute_status_distribution(tickets: List[Dict]) -> List[Dict[str, Any]]:
    if not tickets:
        return []
    status_count = {}
    for t in tickets:
        status = t.get("status", "Unknown")
        status_count[status] = status_count.get(status, 0) + 1
    return [{"status": status, "count": count} for status, count in status_count.items()]


def compute_sentiment_distribution(tickets: List[Dict]) -> List[Dict[str, Any]]:
    if not tickets:
        return []
    sent_count = {}
    for t in tickets:
        sent = t.get("sentiment", "")
        if sent:  # only count non-empty sentiment
            sent_count[sent] = sent_count.get(sent, 0) + 1
    return [{"sentiment": sent, "count": count} for sent, count in sent_count.items()]


def compute_intent_distribution(tickets: List[Dict]) -> List[Dict[str, Any]]:
    if not tickets:
        return []
    intent_count = {}
    for t in tickets:
        intent = t.get("intent", "")
        if intent:  # only count non-empty intent
            intent_count[intent] = intent_count.get(intent, 0) + 1
    return [{"intent": intent, "count": count} for intent, count in intent_count.items()]


def compute_ticket_trends_daily(tickets: List[Dict], days: int = 30) -> List[Dict[str, Any]]:
    if not tickets:
        return []
    # Filter tickets from the last 'days' days
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_tickets = []
    for t in tickets:
        created_at = t.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except ValueError:
                continue
        if created_at and created_at >= cutoff_date:
            recent_tickets.append(t)
    # Group by day
    day_count = {}
    for t in recent_tickets:
        created_at = t.get("created_at")
        if isinstance(created_at, str):
            day = created_at.split("T")[0]  # YYYY-MM-DD
        else:
            day = created_at.strftime("%Y-%m-%d")
        day_count[day] = day_count.get(day, 0) + 1
    # Sort by day
    sorted_days = sorted(day_count.keys())
    return [{"day": day, "count": day_count[day]} for day in sorted_days]


def compute_ticket_trends_monthly(tickets: List[Dict], months: int = 6) -> List[Dict[str, Any]]:
    if not tickets:
        return []
    # Filter tickets from the last 'months' months
    cutoff_date = datetime.now() - timedelta(days=30*months)
    recent_tickets = []
    for t in tickets:
        created_at = t.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except ValueError:
                continue
        if created_at and created_at >= cutoff_date:
            recent_tickets.append(t)
    # Group by month (YYYY-MM)
    month_count = {}
    for t in recent_tickets:
        created_at = t.get("created_at")
        if isinstance(created_at, str):
            month = created_at[:7]  # YYYY-MM
        else:
            month = created_at.strftime("%Y-%m")
        month_count[month] = month_count.get(month, 0) + 1
    # Sort by month
    sorted_months = sorted(month_count.keys())
    return [{"month": month, "count": month_count[month]} for month in sorted_months]


def compute_resolution_trends(tickets: List[Dict], days: int = 30) -> List[Dict[str, Any]]:
    if not tickets:
        return []
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_tickets = []
    for t in tickets:
        created_at = t.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except ValueError:
                continue
        if created_at and created_at >= cutoff_date:
            recent_tickets.append(t)
    # Group by day
    day_stats = {}
    for t in recent_tickets:
        created_at = t.get("created_at")
        if isinstance(created_at, str):
            day = created_at.split("T")[0]
        else:
            day = created_at.strftime("%Y-%m-%d")
        if day not in day_stats:
            day_stats[day] = {"total": 0, "resolved": 0}
        day_stats[day]["total"] += 1
        if t.get("status") == "Resolved":
            day_stats[day]["resolved"] += 1
    # Sort by day
    sorted_days = sorted(day_stats.keys())
    return [
        {
            "day": day,
            "total": day_stats[day]["total"],
            "resolved": day_stats[day]["resolved"],
        }
        for day in sorted_days
    ]


def compute_resolution_summary(tickets: List[Dict]) -> Dict[str, Any]:
    if not tickets:
        return {
            "total": 0,
            "resolved": 0,
            "resolution_rate": 0,
            "avg_days_open": 0,
        }
    total = len(tickets)
    resolved = sum(1 for t in tickets if t.get("status") == "Resolved")
    resolution_rate = round((resolved / total) * 100, 2) if total > 0 else 0
    # Average days open (for all tickets, resolved or not)
    total_days = 0
    count_with_date = 0
    for t in tickets:
        created_at = t.get("created_at")
        if created_at:
            if isinstance(created_at, str):
                try:
                    created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                except ValueError:
                    continue
            days_open = (datetime.now() - created_at).days
            total_days += days_open
            count_with_date += 1
    avg_days_open = round(total_days / count_with_date, 2) if count_with_date > 0 else 0
    return {
        "total": total,
        "resolved": resolved,
        "resolution_rate": resolution_rate,
        "avg_days_open": avg_days_open,
    }


def compute_average_satisfaction_score(tickets: List[Dict]) -> float:
    if not tickets:
        return 0.0
    _SCORE_MAP = {"Positive": 5, "Neutral": 3, "Negative": 1}
    scores = []
    for t in tickets:
        sent = t.get("sentiment", "")
        if sent in _SCORE_MAP:
            scores.append(_SCORE_MAP[sent])
    return round(sum(scores) / len(scores), 2) if scores else 0.0


def compute_rating_distribution(tickets: List[Dict]) -> Dict[str, int]:
    if not tickets:
        return {}
    _SCORE_MAP = {"Positive": 5, "Neutral": 3, "Negative": 1}
    sent_count = {}
    for t in tickets:
        sent = t.get("sentiment", "")
        if sent:
            sent_count[sent] = sent_count.get(sent, 0) + 1
    # Map sentiment to rating label for display? We'll return sentiment counts as before.
    return sent_count


def compute_satisfaction_trend(tickets: List[Dict]) -> List[Dict[str, Any]]:
    if not tickets:
        return []
    _SCORE_MAP = {"Positive": 5, "Neutral": 3, "Negative": 1}
    # Group by month
    month_data = {}
    for t in tickets:
        created_at = t.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except ValueError:
                continue
        if not created_at:
            continue
        month = created_at.strftime("%Y-%m")
        sent = t.get("sentiment", "")
        if sent in _SCORE_MAP:
            score = _SCORE_MAP[sent]
            if month not in month_data:
                month_data[month] = {"total_score": 0, "count": 0}
            month_data[month]["total_score"] += score
            month_data[month]["count"] += 1
    # Compute average and sort by month
    result = []
    for month in sorted(month_data.keys()):
        total_score = month_data[month]["total_score"]
        count = month_data[month]["count"]
        avg_score = round(total_score / count, 2) if count > 0 else 0
        result.append({
            "month": month,
            "avg_score": avg_score,
            "count": count,
        })
    return result


def compute_top_issues(tickets: List[Dict], limit: int = 10) -> List[Dict[str, Any]]:
    if not tickets:
        return []
    intent_count = {}
    for t in tickets:
        intent = t.get("intent", "")
        if intent:
            intent_count[intent] = intent_count.get(intent, 0) + 1
    # Sort by count descending and take top limit
    sorted_intents = sorted(intent_count.items(), key=lambda x: x[1], reverse=True)[:limit]
    return [{"intent": intent, "count": count} for intent, count in sorted_intents]


def get_filter_options() -> Dict[str, List[str]]:
    """Get unique filter options from all tickets (unfiltered)."""
    all_tickets = get_all_tickets()  # no filters
    departments = sorted({t.get("department", "Unknown") for t in all_tickets if t.get("department")})
    priorities = sorted({t.get("priority", "Unknown") for t in all_tickets if t.get("priority")})
    statuses = sorted({t.get("status", "Unknown") for t in all_tickets if t.get("status")})
    return {
        "departments": departments,
        "priorities": priorities,
        "statuses": statuses,
    }


# --- Filter Section ---
st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
with st.container():
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;"
        f"margin-bottom:.4rem;'>🔍 Filters</div>",
        unsafe_allow_html=True,
    )
    f1, f2, f3, f4 = st.columns([2, 2, 2, 1])

    # Initialize filter state in session state if not present
    if "analytics_dept_filter" not in st.session_state:
        st.session_state.analytics_dept_filter = []
    if "analytics_pri_filter" not in st.session_state:
        st.session_state.analytics_pri_filter = []
    if "analytics_status_filter" not in st.session_state:
        st.session_state.analytics_status_filter = []

    # Get filter options
    filter_options = get_filter_options()

    with f1:
        dept_options = filter_options["departments"]
        selected_depts = st.multiselect(
            "Department",
            options=dept_options,
            default=st.session_state.analytics_dept_filter,
            key="analytics_dept_multiselect",
        )
        st.session_state.analytics_dept_filter = selected_depts
    with f2:
        pri_options = filter_options["priorities"]
        selected_pris = st.multiselect(
            "Priority",
            options=pri_options,
            default=st.session_state.analytics_pri_filter,
            key="analytics_pri_multiselect",
        )
        st.session_state.analytics_pri_filter = selected_pris
    with f3:
        status_options = filter_options["statuses"]
        selected_statuses = st.multiselect(
            "Status",
            options=status_options,
            default=st.session_state.analytics_status_filter,
            key="analytics_status_multiselect",
        )
        st.session_state.analytics_status_filter = selected_statuses
    with f4:
        st.markdown("<br>", unsafe_allow_html=True)  # spacer for alignment
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.analytics_dept_filter = []
            st.session_state.analytics_pri_filter = []
            st.session_state.analytics_status_filter = []
            st.rerun()

# Fetch filtered tickets based on selected filters
dept_filter = st.session_state.analytics_dept_filter if st.session_state.analytics_dept_filter else None
pri_filter = st.session_state.analytics_pri_filter if st.session_state.analytics_pri_filter else None
status_filter = st.session_state.analytics_status_filter if st.session_state.analytics_status_filter else None

filtered_tickets = get_all_tickets(
    department=dept_filter,
    priority=pri_filter,
    status=status_filter,
)

# If no filters selected, we show all tickets (already handled by None)

# Compute analytics from filtered tickets
dept_dist = compute_department_distribution(filtered_tickets)
pri_dist = compute_priority_distribution(filtered_tickets)
status_dist = compute_status_distribution(filtered_tickets)
sent_dist = compute_sentiment_distribution(filtered_tickets)
intent_dist = compute_intent_distribution(filtered_tickets)
ticket_trends_daily = compute_ticket_trends_daily(filtered_tickets, days=30)
ticket_trends_monthly = compute_ticket_trends_monthly(filtered_tickets, months=6)
resolution_trends = compute_resolution_trends(filtered_tickets, days=30)
resolution_summary = compute_resolution_summary(filtered_tickets)
avg_satisfaction = compute_average_satisfaction_score(filtered_tickets)
rating_dist = compute_rating_distribution(filtered_tickets)
satisfaction_trend = compute_satisfaction_trend(filtered_tickets)
top_issues = compute_top_issues(filtered_tickets, limit=10)

# ── Summary KPIs ──────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1: metric_card("Total Tickets",      resolution_summary["total"],                  "🎫", COLORS["primary"])
with k2: metric_card("Resolution Rate",    f"{resolution_summary['resolution_rate']}%", "✅", COLORS["green"])
with k3: metric_card("Avg Days Open",      f"{resolution_summary['avg_days_open']}d",   "📅", COLORS["orange"])
with k4: metric_card("Satisfaction Score", f"{avg_satisfaction}/5",                   "⭐", COLORS["cyan"])

st.markdown("<div style='height:.8rem;'></div>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distribution",
    "📈 Trends",
    "🏢 Departments",
    "😊 Sentiment & Intent",
    "⭐ Satisfaction",
])

# ─── TAB 1: Distribution ──────────────────────────────────────────────────────
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        _wrap("Department Distribution")
        if dept_dist:
            fig = go.Figure(go.Pie(
                labels=[d["department"] for d in dept_dist],
                values=[d["count"] for d in dept_dist],
                hole=.48,
                marker=dict(colors=CHART_COLORS, line=dict(color=COLORS["bg"], width=2)),
                textfont=dict(color="white", size=11),
            ))
            st.plotly_chart(_dl(fig, 310), use_container_width=True)
        else:
            st.info("No data yet.")

    with c2:
        _wrap("Priority Distribution")
        if pri_dist:
            fig2 = go.Figure(go.Bar(
                x=[d["priority"] for d in pri_dist],
                y=[d["count"] for d in pri_dist],
                marker_color=[PRIORITY_COLORS.get(d["priority"], COLORS["primary"]) for d in pri_dist],
                text=[d["count"] for d in pri_dist],
                textposition="outside",
                textfont=dict(color="white", size=12),
            ))
            fig2.update_layout(bargap=0.4)
            st.plotly_chart(_dl(fig2, 310), use_container_width=True)
        else:
            st.info("No data yet.")

    st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        _wrap("Status Distribution")
        if status_dist:
            fig3 = go.Figure(go.Pie(
                labels=[d["status"] for d in status_dist],
                values=[d["count"] for d in status_dist],
                hole=.48,
                marker=dict(
                    colors=[STATUS_COLORS.get(d["status"], COLORS["muted"]) for d in status_dist],
                    line=dict(color=COLORS["bg"], width=2),
                ),
                textfont=dict(color="white", size=12),
            ))
            st.plotly_chart(_dl(fig3, 280), use_container_width=True)
        else:
            st.info("No data yet.")

    with c4:
        _wrap("Top Issue Categories")
        if top_issues:
            fig4 = go.Figure(go.Bar(
                x=[i["count"] for i in top_issues],
                y=[i["intent"] for i in top_issues],
                orientation="h",
                marker_color=CHART_COLORS[:len(top_issues)],
                text=[i["count"] for i in top_issues],
                textposition="outside",
                textfont=dict(color="white", size=11),
            ))
            st.plotly_chart(_dl(fig4, 280), use_container_width=True)
        else:
            st.info("No intent data yet.")

# ─── TAB 2: Trends ────────────────────────────────────────────────────────────
with tab2:
    _wrap("Daily Ticket Volume", "last 30 days")
    if ticket_trends_daily:
        df_t = pd.DataFrame(ticket_trends_daily)
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=df_t["day"], y=df_t["count"],
            mode="lines+markers",
            line=dict(color=COLORS["primary"], width=2.5, shape="spline"),
            marker=dict(size=6, color=COLORS["accent"]),
            fill="tozeroy",
            fillcolor=_rgba(COLORS["primary"], 0.13),
            name="Tickets",
        ))
        st.plotly_chart(_dl(fig5, 340), use_container_width=True)
    else:
        st.info("Not enough data for trend chart yet. Raise a few tickets first.")

    st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
    _wrap("Monthly Ticket Trends", "last 6 months")
    if ticket_trends_monthly:
        df_m = pd.DataFrame(ticket_trends_monthly)
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(
            x=df_m["month"], y=df_m["count"],
            mode="lines+markers",
            line=dict(color=COLORS["cyan"], width=2.5, shape="spline"),
            marker=dict(size=6, color=COLORS["accent"]),
            fill="tozeroy",
            fillcolor=_rgba(COLORS["cyan"], 0.13),
            name="Tickets per Month",
        ))
        st.plotly_chart(_dl(fig6, 340), use_container_width=True)
    else:
        st.info("Not enough data for monthly trend yet.")

    st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
    _wrap("Resolved vs Total Tickets", "last 30 days")
    if resolution_trends:
        df_r = pd.DataFrame(resolution_trends)
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(x=df_r["day"], y=df_r["total"],
                              name="Total", marker_color=_rgba(COLORS["blue"], 0.6)))
        fig7.add_trace(go.Bar(x=df_r["day"], y=df_r["resolved"],
                              name="Resolved", marker_color=COLORS["green"]))
        fig7.update_layout(barmode="overlay")
        st.plotly_chart(_dl(fig7, 300), use_container_width=True)
    else:
        st.info("Not enough resolution trend data yet.")

# ─── TAB 3: Departments ───────────────────────────────────────────────────────
with tab3:
    _wrap("Department Performance — Stacked Bar")
    # Compute department performance from filtered tickets
    dept_perf = {}
    for t in filtered_tickets:
        dept = t.get("department", "Unknown")
        status = t.get("status", "Unknown")
        if dept not in dept_perf:
            dept_perf[dept] = {"resolved": 0, "in_progress": 0, "pending": 0}
        if status == "Resolved":
            dept_perf[dept]["resolved"] += 1
        elif status == "In Progress":
            dept_perf[dept]["in_progress"] += 1
        elif status == "Pending":
            dept_perf[dept]["pending"] += 1
        # Note: we are ignoring other statuses if any
    if dept_perf:
        df_d = pd.DataFrame([
            {"department": dept, **counts}
            for dept, counts in dept_perf.items()
        ])
        fig8 = go.Figure()
        for col, color, name in [
            ("resolved",    COLORS["green"],  "Resolved"),
            ("in_progress", COLORS["blue"],   "In Progress"),
            ("pending",     COLORS["orange"], "Pending"),
        ]:
            if col in df_d.columns:
                fig8.add_trace(go.Bar(
                    x=df_d["department"], y=df_d[col],
                    name=name, marker_color=color,
                ))
        fig8.update_layout(barmode="stack", bargap=0.3)
        st.plotly_chart(_dl(fig8, 340), use_container_width=True)

        st.markdown("<div style='height:.4rem;'></div>", unsafe_allow_html=True)
        _wrap("Average Days Open per Department", "unresolved tickets")
        # Compute average days open per department for unresolved tickets
        dept_days = {}
        dept_counts = {}
        for t in filtered_tickets:
            if t.get("status") != "Resolved":
                dept = t.get("department", "Unknown")
                created_at = t.get("created_at")
                if created_at:
                    if isinstance(created_at, str):
                        try:
                            created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                        except ValueError:
                            continue
                    days_open = (datetime.now() - created_at).days
                    if dept not in dept_days:
                        dept_days[dept] = 0
                        dept_counts[dept] = 0
                    dept_days[dept] += days_open
                    dept_counts[dept] += 1
        avg_dept_days = {}
        for dept in dept_days:
            if dept_counts[dept] > 0:
                avg_dept_days[dept] = round(dept_days[dept] / dept_counts[dept], 2)
        if avg_dept_days:
            fig9 = go.Figure(go.Bar(
                x=[avg_dept_days[dept] for dept in avg_dept_days],
                y=[dept for dept in avg_dept_days],
                orientation="h",
                marker_color=COLORS["orange"],
                text=[f"{avg_dept_days[dept]}d" for dept in avg_dept_days],
                textposition="outside",
                textfont=dict(color="white"),
            ))
            st.plotly_chart(_dl(fig9, 260), use_container_width=True)

        st.markdown("<div style='height:.4rem;'></div>", unsafe_allow_html=True)
        df_d_show = df_d.copy()
        df_d_show.columns = [c.replace("_", " ").title() for c in df_d_show.columns]
        st.dataframe(df_d_show, use_container_width=True, hide_index=True)
    else:
        st.info("No department data yet.")

# ─── TAB 4: Sentiment & Intent ────────────────────────────────────────────────
with tab4:
    sc1, sc2 = st.columns(2)

    with sc1:
        _wrap("Sentiment Distribution")
        if sent_dist:
            fig10 = go.Figure(go.Pie(
                labels=[d["sentiment"] for d in sent_dist],
                values=[d["count"] for d in sent_dist],
                hole=.48,
                marker=dict(
                    colors=[SENTIMENT_COLORS.get(d["sentiment"], COLORS["muted"]) for d in sent_dist],
                    line=dict(color=COLORS["bg"], width=2),
                ),
                textfont=dict(color="white", size=12),
            ))
            st.plotly_chart(_dl(fig10, 300), use_container_width=True)

            total_s = sum(d["count"] for d in sent_dist)
            cols = st.columns(len(sent_dist))
            for col, d in zip(cols, sent_dist):
                pct = round(d["count"] / total_s * 100, 1) if total_s else 0
                color = SENTIMENT_COLORS.get(d["sentiment"], COLORS["muted"])
                with col:
                    st.markdown(f"""
                    <div style="background:{color}22;border:1px solid {color}55;
                        border-radius:10px;padding:.5rem;text-align:center;">
                        <div style="color:{color};font-weight:700;font-size:1.1rem;">{pct}%</div>
                        <div style="color:{_c_muted};font-size:.72rem;">{d['sentiment']}</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("No sentiment data yet.")

    with sc2:
        _wrap("Intent / Query Category Distribution")
        if intent_dist:
            fig11 = go.Figure(go.Bar(
                x=[d["count"] for d in intent_dist],
                y=[d["intent"] for d in intent_dist],
                orientation="h",
                marker=dict(
                    color=list(range(len(intent_dist))),
                    colorscale=[[0, COLORS["primary"]], [1, COLORS["cyan"]]],
                ),
                text=[d["count"] for d in intent_dist],
                textposition="outside",
                textfont=dict(color="white", size=11),
            ))
            st.plotly_chart(_dl(fig11, 340), use_container_width=True)
        else:
            st.info("No intent data yet.")

# ─── TAB 5: Satisfaction ─────────────────────────────────────────────────────
with tab5:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{COLORS['card']},{COLORS['card2']});
        border:1px solid {COLORS['border']};border-radius:18px;padding:1.4rem;
        text-align:center;margin-bottom:1.2rem;">
        <div style="color:{_c_muted};font-size:.75rem;font-weight:700;
            text-transform:uppercase;letter-spacing:.08em;">Average Satisfaction Score</div>
        <div style="color:{COLORS['green']};font-size:3.5rem;font-weight:800;
            line-height:1;">{avg_satisfaction}</div>
        <div style="color:{_c_muted};font-size:.85rem;">out of 5.0</div>
        <div style="color:{'#F59E0B' if avg_satisfaction < 3 else '#22C55E'};font-size:.85rem;
            margin-top:.3rem;">{'⚠️ Needs improvement' if avg_satisfaction < 3 else '✅ Good'}</div>
    </div>""", unsafe_allow_html=True)

    sa1, sa2 = st.columns(2)

    with sa1:
        _wrap("Rating Distribution (by Sentiment)")
        if rating_dist:
            fig12 = go.Figure(go.Bar(
                x=list(rating_dist.keys()),
                y=list(rating_dist.values()),
                marker_color=[SENTIMENT_COLORS.get(k, COLORS["muted"]) for k in rating_dist.keys()],
                text=list(rating_dist.values()),
                textposition="outside",
                textfont=dict(color="white", size=12),
            ))
            fig12.update_layout(bargap=0.4)
            st.plotly_chart(_dl(fig12, 280), use_container_width=True)
        else:
            st.info("No rating data yet.")

    with sa2:
        _wrap("Monthly Satisfaction Trend")
        if satisfaction_trend:
            df_st = pd.DataFrame(satisfaction_trend)
            fig13 = go.Figure()
            fig13.add_trace(go.Scatter(
                x=df_st["month"], y=df_st["avg_score"],
                mode="lines+markers",
                line=dict(color=COLORS["green"], width=2.5, shape="spline"),
                marker=dict(size=8, color=COLORS["cyan"]),
                fill="tozeroy",
                fillcolor=_rgba(COLORS["green"], 0.13),
                name="Avg Score",
            ))
            fig13.add_hline(y=3, line_dash="dash",
                            line_color=COLORS["orange"], opacity=0.6,
                            annotation_text="Neutral (3)",
                            annotation_font_color=COLORS["orange"])
            st.plotly_chart(_dl(fig13, 280), use_container_width=True)
        else:
            st.info("Not enough monthly data yet.")