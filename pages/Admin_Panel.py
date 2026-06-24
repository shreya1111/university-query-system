import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from collections import Counter, defaultdict
from datetime import datetime as dt
from core.config import APP_ICON
from core.database import (
    initialize_database,
    get_tickets_filtered,
    get_all_tickets,
    update_ticket_status,
)
from features.notifications.service import get_notifications, unread_count
from components.sidebar import render_sidebar
from components.cards import page_header
from components.metric_card import metric_card
from components.notification_card import notification_item
from styles.custom_css import inject_css
from styles.theme import COLORS, CHART_COLORS, PRIORITY_COLORS, STATUS_COLORS, SENTIMENT_COLORS

st.set_page_config(page_title="Admin Panel", page_icon="🛡️", layout="wide")
inject_css()
initialize_database()
render_sidebar()
page_header("🛡️ Admin Panel", "System-wide oversight, KPIs, and operational intelligence.")

_c_text   = COLORS["text"]
_c_muted  = COLORS["muted"]
_c_orange = COLORS["orange"]


def _dark_layout(fig, height=280):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["muted"], family="Inter"),
        margin=dict(t=20, b=10, l=10, r=10), height=height,
        legend=dict(font=dict(color=COLORS["muted"], size=10), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor=COLORS["border_solid"], color=COLORS["muted"]),
        yaxis=dict(gridcolor=COLORS["border_solid"], color=COLORS["muted"]),
    )
    return fig


def _info_card(label, value, color):
    st.markdown(
        f'<div style="background:{COLORS["card2"]};border:1px solid {COLORS["border"]};'
        f'border-left:3px solid {color};border-radius:12px;padding:.75rem 1rem;margin-bottom:.5rem;">'
        f'<div style="color:{COLORS["muted"]};font-size:.68rem;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:.07em;">{label}</div>'
        f'<div style="color:{color};font-weight:700;font-size:.97rem;margin-top:.2rem;">{value}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Session state defaults (BEFORE any widgets) ───────────────────────────────
# FIX: only set defaults; never reassign after widget renders with same key
_DEFAULTS = {
    "admin_dept_filter":         [],
    "admin_pri_filter":          [],
    "admin_status_filter":       [],
    "admin_sentiment_filter":    [],
    "admin_intent_filter":       [],
    "admin_search_ticket_id":    "",
    "admin_search_student_name": "",
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Filter options ────────────────────────────────────────────────────────────
all_tickets       = get_all_tickets()
dept_options      = sorted({t.get("department","") for t in all_tickets if t.get("department")})
pri_options       = sorted({t.get("priority","")   for t in all_tickets if t.get("priority")})
status_options    = sorted({t.get("status","")     for t in all_tickets if t.get("status")})
sentiment_options = sorted({t.get("sentiment","")  for t in all_tickets if t.get("sentiment")})
intent_options    = sorted({t.get("intent","")     for t in all_tickets if t.get("intent")})

# ── Filter row ────────────────────────────────────────────────────────────────
st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
st.markdown(
    f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;margin-bottom:.4rem;'>"
    f"🔍 Filters &amp; Search</div>",
    unsafe_allow_html=True,
)

f1, f2, f3, f4, f5, f6, f7 = st.columns([2, 2, 2, 2, 2, 2, 1])
with f1:
    st.multiselect("Department", options=dept_options,
                   default=st.session_state.admin_dept_filter,
                   key="admin_dept_filter")
with f2:
    st.multiselect("Priority", options=pri_options,
                   default=st.session_state.admin_pri_filter,
                   key="admin_pri_filter")
with f3:
    st.multiselect("Status", options=status_options,
                   default=st.session_state.admin_status_filter,
                   key="admin_status_filter")
with f4:
    st.multiselect("Sentiment", options=sentiment_options,
                   default=st.session_state.admin_sentiment_filter,
                   key="admin_sentiment_filter")
with f5:
    st.multiselect("Intent", options=intent_options,
                   default=st.session_state.admin_intent_filter,
                   key="admin_intent_filter")
with f6:
    st.text_input("Ticket ID", placeholder="e.g., 123",
                  key="admin_search_ticket_id")
with f7:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reset", use_container_width=True):
        for k in _DEFAULTS:
            st.session_state.pop(k, None)
        st.rerun()

s1, s2, s3 = st.columns([6, 2, 2])
with s1:
    st.text_input("Student Name", placeholder="e.g., John Smith",
                  key="admin_search_student_name")
with s2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 Search", use_container_width=True):
        st.rerun()
with s3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🧹 Clear Search", use_container_width=True):
        st.session_state.pop("admin_search_ticket_id", None)
        st.session_state.pop("admin_search_student_name", None)
        st.rerun()

# ── Read values from session state ───────────────────────────────────────────
dept_filter      = st.session_state.admin_dept_filter      or None
pri_filter       = st.session_state.admin_pri_filter       or None
status_filter    = st.session_state.admin_status_filter    or None
sentiment_filter = st.session_state.admin_sentiment_filter or None
intent_filter    = st.session_state.admin_intent_filter    or None
search_ticket_id    = st.session_state.admin_search_ticket_id.strip()    or None
search_student_name = st.session_state.admin_search_student_name.strip() or None

filtered_tickets = get_tickets_filtered(
    department=dept_filter, priority=pri_filter, status=status_filter,
    sentiment=sentiment_filter, intent=intent_filter,
    search_ticket_id=search_ticket_id, search_student_name=search_student_name,
)

st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
total    = len(filtered_tickets)
pending  = sum(1 for t in filtered_tickets if t.get("status") == "Pending")
in_prog  = sum(1 for t in filtered_tickets if t.get("status") == "In Progress")
resolved = sum(1 for t in filtered_tickets if t.get("status") == "Resolved")
high_pri = sum(1 for t in filtered_tickets if t.get("priority") == "High")
res_rate = round(resolved / total * 100, 1) if total else 0.0

k1,k2,k3,k4,k5,k6 = st.columns(6)
with k1: metric_card("Total Tickets",   total,          "🎫", COLORS["primary"])
with k2: metric_card("Pending",         pending,        "⏳", COLORS["orange"])
with k3: metric_card("In Progress",     in_prog,        "🔄", COLORS["blue"])
with k4: metric_card("Resolved",        resolved,       "✅", COLORS["green"])
with k5: metric_card("High Priority",   high_pri,       "🔴", COLORS["red"])
with k6: metric_card("Resolution Rate", f"{res_rate}%", "📈", COLORS["cyan"])

st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
dept_dist   = [{"department": d, "count": c}
               for d,c in Counter(t.get("department","") for t in filtered_tickets).items() if d]
intent_dist = [{"intent": i, "count": c}
               for i,c in Counter(t.get("intent","") for t in filtered_tickets).items() if i]

dept_counts_map  = {d["department"]: d["count"] for d in dept_dist}
most_active_dept = max(dept_counts_map, key=dept_counts_map.get) if dept_counts_map else "N/A"

dept_days: dict = defaultdict(list)
for t in filtered_tickets:
    if t.get("status") == "Resolved" and t.get("department") and t.get("created_at"):
        try:
            days = (dt.now() - dt.fromisoformat(str(t["created_at"])[:19])).days
            dept_days[t["department"]].append(days)
        except Exception:
            pass
avg_days     = {d: sum(v)/len(v) for d, v in dept_days.items() if v}
fastest_dept = min(avg_days, key=avg_days.get) if avg_days else "N/A"
slowest_dept = max(avg_days, key=avg_days.get) if avg_days else "N/A"

ch_left, ch_mid, ch_right = st.columns([2, 2, 1])

with ch_left:
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;margin-bottom:.4rem;'>"
        f"🏢 Department Ticket Distribution</div>", unsafe_allow_html=True)
    if dept_dist:
        fig_pie = go.Figure(go.Pie(
            labels=[d["department"] for d in dept_dist],
            values=[d["count"]      for d in dept_dist],
            hole=.48,
            marker=dict(colors=CHART_COLORS, line=dict(color=COLORS["bg"], width=2)),
            textfont=dict(color="white", size=10),
        ))
        st.plotly_chart(_dark_layout(fig_pie, 280), use_container_width=True)
    else:
        st.info("No data yet.")

with ch_mid:
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;margin-bottom:.4rem;'>"
        f"🔥 Top Issue Categories</div>", unsafe_allow_html=True)
    if intent_dist:
        fig_bar = go.Figure(go.Bar(
            x=[i["count"]  for i in intent_dist],
            y=[i["intent"] for i in intent_dist],
            orientation="h",
            marker_color=CHART_COLORS[:len(intent_dist)],
            text=[i["count"] for i in intent_dist],
            textposition="outside",
            textfont=dict(color="white", size=11),
        ))
        st.plotly_chart(_dark_layout(fig_bar, 280), use_container_width=True)
    else:
        st.info("No intent data yet.")

with ch_right:
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;margin-bottom:.7rem;'>"
        f"⚡ Quick Stats</div>", unsafe_allow_html=True)
    _info_card("Most Active Dept",   most_active_dept, COLORS["primary"])
    _info_card("Fastest Resolution", fastest_dept,     COLORS["green"])
    _info_card("Needs Attention",    slowest_dept,     COLORS["red"])
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;margin-bottom:.6rem;'>"
        f"🔔 Notifications <span style='color:{_c_orange};font-size:.78rem;'>"
        f"({unread_count()})</span></div>",
        unsafe_allow_html=True,
    )
    notifs = get_notifications(8)
    if notifs:
        for n in notifs:
            notification_item(n["message"], n.get("timestamp",""), icon="🔔", color=COLORS["primary"])
    else:
        st.info("No notifications yet.")

st.markdown("<hr>", unsafe_allow_html=True)

# ── Ticket table ──────────────────────────────────────────────────────────────
st.markdown(
    f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;margin-bottom:.6rem;'>"
    f"🎫 Ticket Management</div>", unsafe_allow_html=True)

if not filtered_tickets:
    st.info("No tickets match the current filters.")
else:
    for ticket in filtered_tickets:
        tid = ticket["ticket_id"]
        if tid != filtered_tickets[0]["ticket_id"]:
            st.markdown("<hr style='margin:0.5rem 0;'>", unsafe_allow_html=True)

        t1,t2,t3,t4,t5,t6,t7,t8,t9 = st.columns([1,2,2,2,2,2,2,2,2])
        with t1: st.write(f"**{tid}**")
        with t2: st.write(ticket.get("student_name",""))
        with t3: st.write(ticket.get("department",""))
        with t4:
            pri = ticket.get("priority","")
            st.markdown(f"<span style='color:{PRIORITY_COLORS.get(pri, _c_muted)};font-weight:bold;'>{pri}</span>", unsafe_allow_html=True)
        with t5:
            sta = ticket.get("status","")
            st.markdown(f"<span style='color:{STATUS_COLORS.get(sta, _c_muted)};font-weight:bold;'>{sta}</span>", unsafe_allow_html=True)
        with t6: st.write(ticket.get("intent",""))
        with t7:
            sent = ticket.get("sentiment","")
            st.markdown(f"<span style='color:{SENTIMENT_COLORS.get(sent, _c_muted)};font-weight:bold;'>{sent}</span>", unsafe_allow_html=True)
        with t8: st.write(str(ticket.get("created_at",""))[:16])
        with t9:
            a1, a2 = st.columns(2)
            with a1:
                cur = ticket.get("status","Pending")
                opts = ["Pending","In Progress","Resolved"]
                new_s = st.selectbox("Status", opts,
                                     index=opts.index(cur) if cur in opts else 0,
                                     key=f"status_{tid}",
                                     label_visibility="collapsed")
                if new_s != cur and st.button("💾", key=f"update_{tid}", use_container_width=True):
                    update_ticket_status(tid, new_s)
                    st.success(f"#{tid} → {new_s}")
                    st.rerun()
            with a2:
                dk = f"show_details_{tid}"
                if st.button("🔍", key=f"details_{tid}", use_container_width=True):
                    st.session_state[dk] = not st.session_state.get(dk, False)
                    st.rerun()

        if st.session_state.get(f"show_details_{tid}", False):
            d1, d2 = st.columns(2)
            with d1:
                st.markdown("**AI Summary**")
                st.write(ticket.get("summary","No summary available"))
            with d2:
                st.markdown("**Auto Reply**")
                st.write(ticket.get("auto_reply","No auto reply available"))

st.markdown("<hr>", unsafe_allow_html=True)

with st.expander("📊 Department Performance Breakdown"):
    dept_perf: dict = {}
    for t in filtered_tickets:
        dept, status = t.get("department","Unknown"), t.get("status","Unknown")
        if dept not in dept_perf:
            dept_perf[dept] = {"resolved":0,"in_progress":0,"pending":0}
        if   status == "Resolved":   dept_perf[dept]["resolved"]    += 1
        elif status == "In Progress":dept_perf[dept]["in_progress"] += 1
        elif status == "Pending":    dept_perf[dept]["pending"]     += 1
    if dept_perf:
        df_d = pd.DataFrame([{"department":d,**c} for d,c in dept_perf.items()])
        df_d.columns = [c.replace("_"," ").title() for c in df_d.columns]
        st.dataframe(df_d, use_container_width=True, hide_index=True)
    else:
        st.info("No department data yet.")
