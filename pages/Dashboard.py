import streamlit as st
import plotly.graph_objects as go
from core.config import APP_ICON, THEME, PRIORITY_COLORS, STATUS_COLORS
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import kpi_card, page_header
from features.ticket_management.service import TicketService

st.set_page_config(page_title="Dashboard", page_icon=APP_ICON, layout="wide")
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"],.main{{background:{THEME['bg']}}}
[data-testid="stSidebar"]{{background:#0D1B2E;border-right:1px solid {THEME['border']}}}
h1,h2,h3{{color:{THEME['text']}}} p,span,li,label{{color:{THEME['muted']}}}
hr{{border-color:{THEME['border']}}} .block-container{{padding:2rem 2rem 1rem}}
</style>""", unsafe_allow_html=True)

initialize_database()
render_sidebar()

svc = TicketService()
stats = svc.dashboard_stats()
dept_data = svc.dept_chart_data()
pri_data = svc.priority_chart_data()

page_header("📊 Dashboard", "Real-time overview of all university queries")

# KPI Row
c1, c2, c3, c4 = st.columns(4)
with c1: kpi_card("Total Tickets",    stats["total"],       THEME["primary"],  "🎫")
with c2: kpi_card("Pending",          stats["pending"],     THEME["warning"],  "⏳")
with c3: kpi_card("In Progress",      stats["in_progress"], THEME["primary"],  "🔄")
with c4: kpi_card("Resolved",         stats["resolved"],    THEME["success"],  "✅")

st.markdown("<br>", unsafe_allow_html=True)

# Charts
col_l, col_r = st.columns(2)

with col_l:
    st.markdown(f"<h3 style='color:{THEME['text']};font-size:1.1rem;margin-bottom:.8rem;'>🏢 Department Distribution</h3>",
                unsafe_allow_html=True)
    if dept_data:
        labels = [d["department"] for d in dept_data]
        values = [d["count"] for d in dept_data]
        fig = go.Figure(go.Pie(
            labels=labels, values=values, hole=.45,
            marker=dict(colors=["#6366F1","#8B5CF6","#06B6D4","#10B981","#F59E0B","#EF4444","#EC4899"]),
            textfont=dict(color="white"),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=THEME["muted"]), margin=dict(t=10,b=10,l=10,r=10),
            legend=dict(font=dict(color=THEME["muted"])),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data yet.")

with col_r:
    st.markdown(f"<h3 style='color:{THEME['text']};font-size:1.1rem;margin-bottom:.8rem;'>⚡ Priority Distribution</h3>",
                unsafe_allow_html=True)
    if pri_data:
        labels = [d["priority"] for d in pri_data]
        values = [d["count"] for d in pri_data]
        colors = [PRIORITY_COLORS.get(p, THEME["primary"]) for p in labels]
        fig2 = go.Figure(go.Bar(
            x=labels, y=values,
            marker_color=colors,
            text=values, textposition="outside",
            textfont=dict(color="white"),
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=THEME["muted"]),
            xaxis=dict(color=THEME["muted"], gridcolor=THEME["border"]),
            yaxis=dict(color=THEME["muted"], gridcolor=THEME["border"]),
            margin=dict(t=30,b=10,l=10,r=10), height=300,
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data yet.")

# Recent tickets table
st.markdown(f"<hr style='border-color:{THEME['border']};'>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color:{THEME['text']};font-size:1.1rem;margin-bottom:.8rem;'>🕐 Recent Tickets</h3>",
            unsafe_allow_html=True)
recent = svc.list_tickets()[:10]
if recent:
    import pandas as pd
    df = pd.DataFrame(recent)[["ticket_id","student_name","department","priority","status","created_at"]]
    df.columns = ["ID","Student","Department","Priority","Status","Created At"]
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No tickets yet. Raise one to get started!")
