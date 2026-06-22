import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from core.config import APP_ICON
from core.database import initialize_database, get_priority_distribution
from components.sidebar import render_sidebar
from components.cards import page_header
from components.metric_card import metric_card
from styles.custom_css import inject_css
from styles.theme import COLORS, CHART_COLORS, PRIORITY_COLORS, STATUS_COLORS, SENTIMENT_COLORS
from features.analytics.ticket_analytics import get_ticket_trends, get_all_tickets_raw
from features.analytics.department_analytics import (
    department_ticket_counts, department_performance, average_resolution_time,
)
from features.analytics.sentiment_analytics import sentiment_distribution, intent_distribution
from features.analytics.resolution_analytics import resolution_trends, resolution_summary
from features.analytics.satisfaction_analytics import (
    average_satisfaction_score, rating_distribution, satisfaction_trend, top_issues,
)

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


# ── Summary KPIs ──────────────────────────────────────────────────────────────
res = resolution_summary()
sat = average_satisfaction_score()
k1, k2, k3, k4 = st.columns(4)
with k1: metric_card("Total Tickets",      res["total"],                  "🎫", COLORS["primary"])
with k2: metric_card("Resolution Rate",    f"{res['resolution_rate']}%", "✅", COLORS["green"])
with k3: metric_card("Avg Days Open",      f"{res['avg_days_open']}d",   "📅", COLORS["orange"])
with k4: metric_card("Satisfaction Score", f"{sat}/5",                   "⭐", COLORS["cyan"])

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
        dept_data = department_ticket_counts()
        if dept_data:
            fig = go.Figure(go.Pie(
                labels=[d["department"] for d in dept_data],
                values=[d["count"] for d in dept_data],
                hole=.48,
                marker=dict(colors=CHART_COLORS, line=dict(color=COLORS["bg"], width=2)),
                textfont=dict(color="white", size=11),
            ))
            st.plotly_chart(_dl(fig, 310), use_container_width=True)
        else:
            st.info("No data yet.")

    with c2:
        _wrap("Priority Distribution")
        pri = get_priority_distribution()
        if pri:
            fig2 = go.Figure(go.Bar(
                x=[d["priority"] for d in pri],
                y=[d["count"] for d in pri],
                marker_color=[PRIORITY_COLORS.get(d["priority"], COLORS["primary"]) for d in pri],
                text=[d["count"] for d in pri],
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
        from core.database import _connect
        with _connect() as conn:
            status_data = [dict(r) for r in conn.execute(
                "SELECT status, COUNT(*) as count FROM tickets GROUP BY status"
            ).fetchall()]
        if status_data:
            fig3 = go.Figure(go.Pie(
                labels=[d["status"] for d in status_data],
                values=[d["count"] for d in status_data],
                hole=.48,
                marker=dict(
                    colors=[STATUS_COLORS.get(d["status"], COLORS["muted"]) for d in status_data],
                    line=dict(color=COLORS["bg"], width=2),
                ),
                textfont=dict(color="white", size=12),
            ))
            st.plotly_chart(_dl(fig3, 280), use_container_width=True)
        else:
            st.info("No data yet.")

    with c4:
        _wrap("Top Issue Categories")
        issues = top_issues()
        if issues:
            fig4 = go.Figure(go.Bar(
                x=[i["count"] for i in issues],
                y=[i["intent"] for i in issues],
                orientation="h",
                marker_color=CHART_COLORS[:len(issues)],
                text=[i["count"] for i in issues],
                textposition="outside",
                textfont=dict(color="white", size=11),
            ))
            st.plotly_chart(_dl(fig4, 280), use_container_width=True)
        else:
            st.info("No intent data yet.")

# ─── TAB 2: Trends ────────────────────────────────────────────────────────────
with tab2:
    _wrap("Daily Ticket Volume", "last 30 days")
    trends = get_ticket_trends()
    if trends:
        df_t = pd.DataFrame(trends)
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=df_t["day"], y=df_t["count"],
            mode="lines+markers",
            line=dict(color=COLORS["primary"], width=2.5, shape="spline"),
            marker=dict(size=6, color=COLORS["accent"]),
            fill="tozeroy",
            fillcolor=COLORS["primary"] + "22",
            name="Tickets",
        ))
        st.plotly_chart(_dl(fig5, 340), use_container_width=True)
    else:
        st.info("Not enough data for trend chart yet. Raise a few tickets first.")

    st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
    _wrap("Resolved vs Total Tickets", "last 30 days")
    res_t = resolution_trends()
    if res_t:
        df_r = pd.DataFrame(res_t)
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(x=df_r["day"], y=df_r["total"],
                              name="Total", marker_color=COLORS["blue"] + "99"))
        fig6.add_trace(go.Bar(x=df_r["day"], y=df_r["resolved"],
                              name="Resolved", marker_color=COLORS["green"]))
        fig6.update_layout(barmode="overlay")
        st.plotly_chart(_dl(fig6, 300), use_container_width=True)
    else:
        st.info("Not enough resolution trend data yet.")

# ─── TAB 3: Departments ───────────────────────────────────────────────────────
with tab3:
    _wrap("Department Performance — Stacked Bar")
    dp = department_performance()
    if dp:
        df_d = pd.DataFrame(dp)
        fig7 = go.Figure()
        for col, color, name in [
            ("resolved",    COLORS["green"],  "Resolved"),
            ("in_progress", COLORS["blue"],   "In Progress"),
            ("pending",     COLORS["orange"], "Pending"),
        ]:
            if col in df_d.columns:
                fig7.add_trace(go.Bar(
                    x=df_d["department"], y=df_d[col],
                    name=name, marker_color=color,
                ))
        fig7.update_layout(barmode="stack", bargap=0.3)
        st.plotly_chart(_dl(fig7, 340), use_container_width=True)

        st.markdown("<div style='height:.4rem;'></div>", unsafe_allow_html=True)
        _wrap("Average Days Open per Department", "unresolved tickets")
        avg_res = average_resolution_time()
        if avg_res:
            fig8 = go.Figure(go.Bar(
                x=[d["avg_days_open"] for d in avg_res],
                y=[d["department"] for d in avg_res],
                orientation="h",
                marker_color=COLORS["orange"],
                text=[f"{d['avg_days_open']}d" for d in avg_res],
                textposition="outside",
                textfont=dict(color="white"),
            ))
            st.plotly_chart(_dl(fig8, 260), use_container_width=True)

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
        sent = sentiment_distribution()
        if sent:
            fig9 = go.Figure(go.Pie(
                labels=[d["sentiment"] for d in sent],
                values=[d["count"] for d in sent],
                hole=.48,
                marker=dict(
                    colors=[SENTIMENT_COLORS.get(d["sentiment"], COLORS["muted"]) for d in sent],
                    line=dict(color=COLORS["bg"], width=2),
                ),
                textfont=dict(color="white", size=12),
            ))
            st.plotly_chart(_dl(fig9, 300), use_container_width=True)

            total_s = sum(d["count"] for d in sent)
            cols = st.columns(len(sent))
            for col, d in zip(cols, sent):
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
        intents = intent_distribution()
        if intents:
            fig10 = go.Figure(go.Bar(
                x=[d["count"] for d in intents],
                y=[d["intent"] for d in intents],
                orientation="h",
                marker=dict(
                    color=list(range(len(intents))),
                    colorscale=[[0, COLORS["primary"]], [1, COLORS["cyan"]]],
                ),
                text=[d["count"] for d in intents],
                textposition="outside",
                textfont=dict(color="white", size=11),
            ))
            st.plotly_chart(_dl(fig10, 340), use_container_width=True)
        else:
            st.info("No intent data yet.")

# ─── TAB 5: Satisfaction ─────────────────────────────────────────────────────
with tab5:
    avg_s = average_satisfaction_score()
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{COLORS['card']},{COLORS['card2']});
        border:1px solid {COLORS['border']};border-radius:18px;padding:1.4rem;
        text-align:center;margin-bottom:1.2rem;">
        <div style="color:{_c_muted};font-size:.75rem;font-weight:700;
            text-transform:uppercase;letter-spacing:.08em;">Average Satisfaction Score</div>
        <div style="color:{COLORS['green']};font-size:3.5rem;font-weight:800;
            line-height:1;">{avg_s}</div>
        <div style="color:{_c_muted};font-size:.85rem;">out of 5.0</div>
        <div style="color:{'#F59E0B' if avg_s < 3 else '#22C55E'};font-size:.85rem;
            margin-top:.3rem;">{'⚠️ Needs improvement' if avg_s < 3 else '✅ Good'}</div>
    </div>""", unsafe_allow_html=True)

    sa1, sa2 = st.columns(2)

    with sa1:
        _wrap("Rating Distribution (by Sentiment)")
        rd = rating_distribution()
        if rd:
            fig11 = go.Figure(go.Bar(
                x=list(rd.keys()),
                y=list(rd.values()),
                marker_color=[SENTIMENT_COLORS.get(k, COLORS["muted"]) for k in rd.keys()],
                text=list(rd.values()),
                textposition="outside",
                textfont=dict(color="white", size=12),
            ))
            fig11.update_layout(bargap=0.4)
            st.plotly_chart(_dl(fig11, 280), use_container_width=True)
        else:
            st.info("No rating data yet.")

    with sa2:
        _wrap("Monthly Satisfaction Trend")
        st_trend = satisfaction_trend()
        if st_trend:
            df_st = pd.DataFrame(st_trend)
            fig12 = go.Figure()
            fig12.add_trace(go.Scatter(
                x=df_st["month"], y=df_st["avg_score"],
                mode="lines+markers",
                line=dict(color=COLORS["green"], width=2.5, shape="spline"),
                marker=dict(size=8, color=COLORS["cyan"]),
                fill="tozeroy",
                fillcolor=COLORS["green"] + "22",
                name="Avg Score",
            ))
            fig12.add_hline(y=3, line_dash="dash",
                            line_color=COLORS["orange"], opacity=0.6,
                            annotation_text="Neutral (3)",
                            annotation_font_color=COLORS["orange"])
            st.plotly_chart(_dl(fig12, 280), use_container_width=True)
        else:
            st.info("Not enough monthly data yet.")