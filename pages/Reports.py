import streamlit as st
import pandas as pd
from datetime import datetime
from core.config import APP_ICON
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from styles.custom_css import inject_css
from styles.theme import COLORS
from features.analytics.reports.csv_export import (
    export_all_tickets, export_department_report,
    export_sentiment_report, export_analytics_csv,
)
from features.analytics.reports.pdf_report import generate_summary_report, save_report
from features.analytics.ticket_analytics import get_all_tickets_raw
from features.analytics.department_analytics import department_performance
from features.analytics.sentiment_analytics import sentiment_distribution, intent_distribution
from features.analytics.resolution_analytics import resolution_summary

st.set_page_config(page_title="Reports", page_icon="📋", layout="wide")
inject_css()
initialize_database()
render_sidebar()
page_header("📋 Reports", "Generate and download analytical reports in CSV and PDF.")


def _card(icon: str, title: str, desc: str, color: str) -> None:
    st.markdown(f"""
    <div style="background:linear-gradient(145deg,{COLORS['card']},{COLORS['card2']});
        border:1px solid {COLORS['border']};border-left:3px solid {color};
        border-radius:16px;padding:1rem 1.2rem;margin-bottom:.4rem;">
        <div style="display:flex;gap:.7rem;align-items:center;">
            <div style="background:{color}22;border:1px solid {color}44;
                border-radius:10px;padding:.5rem;font-size:1.25rem;">{icon}</div>
            <div>
                <div style="color:{COLORS['text']};font-weight:700;font-size:.9rem;">{title}</div>
                <div style="color:{COLORS['muted']};font-size:.76rem;">{desc}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)


today = datetime.now().strftime("%Y%m%d")

# ── CSV Exports ───────────────────────────────────────────────────────────────
st.markdown(f"<div style='color:{COLORS['text']};font-size:.95rem;font-weight:700;"
            f"margin-bottom:.8rem;'>📥 CSV Exports</div>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    _card("🎫", "All Tickets", "Full ticket history with AI fields", COLORS["primary"])
    st.download_button("⬇️ Download", export_all_tickets(),
                       f"tickets_{today}.csv", "text/csv",
                       use_container_width=True, key="dl_all")

with c2:
    _card("🏢", "Department Report", "Performance per department", COLORS["cyan"])
    st.download_button("⬇️ Download", export_department_report(),
                       f"departments_{today}.csv", "text/csv",
                       use_container_width=True, key="dl_dept")

with c3:
    _card("😊", "Sentiment Report", "Sentiment distribution data", COLORS["green"])
    st.download_button("⬇️ Download", export_sentiment_report(),
                       f"sentiment_{today}.csv", "text/csv",
                       use_container_width=True, key="dl_sent")

with c4:
    _card("📊", "Analytics Snapshot", "Combined intent, sentiment & dept", COLORS["orange"])
    st.download_button("⬇️ Download", export_analytics_csv(),
                       f"analytics_{today}.csv", "text/csv",
                       use_container_width=True, key="dl_analytics")

st.markdown("<hr>", unsafe_allow_html=True)

# ── PDF / Generated Reports ───────────────────────────────────────────────────
st.markdown(f"<div style='color:{COLORS['text']};font-size:.95rem;font-weight:700;"
            f"margin-bottom:.8rem;'>📄 Generated Reports</div>", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

with p1:
    _card("📊", "Summary Report", "Ticket stats + department breakdown", COLORS["accent"])
    if st.button("🔄 Generate", use_container_width=True, key="gen_summary"):
        with st.spinner("Generating summary report…"):
            content = generate_summary_report()
            path    = save_report(content, "summary_report")
        ext  = "pdf" if content[:4] == b"%PDF" else "txt"
        mime = "application/pdf" if ext == "pdf" else "text/plain"
        st.success(f"Saved: `{path}`")
        st.download_button(f"⬇️ Download {ext.upper()}", content,
                           f"summary_{today}.{ext}", mime,
                           use_container_width=True, key="dl_summary")

with p2:
    _card("🏢", "Department Report", "Full dept performance breakdown", COLORS["blue"])
    if st.button("🔄 Generate", use_container_width=True, key="gen_dept"):
        with st.spinner("Generating department report…"):
            dp   = department_performance()
            rows = "\n".join(
                f"  {d['department']}: total={d['total']} resolved={d['resolved']} pending={d['pending']}"
                for d in dp
            ) if dp else "  No data."
            content = (
                f"DEPARTMENT PERFORMANCE REPORT\n"
                f"Generated: {datetime.now().strftime('%d %b %Y %H:%M')}\n"
                f"{'='*45}\n{rows}"
            ).encode("utf-8")
            path = save_report(content, "dept_report")
        st.success(f"Saved: `{path}`")
        st.download_button("⬇️ Download TXT", content,
                           f"dept_report_{today}.txt", "text/plain",
                           use_container_width=True, key="dl_dept_pdf")

with p3:
    _card("📅", "Monthly Analytics", "Sentiment + intent monthly summary", COLORS["green"])
    if st.button("🔄 Generate", use_container_width=True, key="gen_monthly"):
        with st.spinner("Generating monthly report…"):
            res  = resolution_summary()
            sent = sentiment_distribution()
            ints = intent_distribution()
            lines = [
                "MONTHLY ANALYTICS REPORT",
                f"Generated: {datetime.now().strftime('%d %b %Y %H:%M')}",
                "=" * 45,
                f"Total Tickets   : {res['total']}",
                f"Resolved        : {res['resolved']}",
                f"Resolution Rate : {res['resolution_rate']}%",
                f"Avg Days Open   : {res['avg_days_open']}",
                "",
                "SENTIMENT BREAKDOWN",
            ] + [f"  {d['sentiment']}: {d['count']}" for d in sent] + [
                "",
                "TOP INTENTS",
            ] + [f"  {d['intent']}: {d['count']}" for d in ints]
            content = "\n".join(lines).encode("utf-8")
            path    = save_report(content, "monthly_report")
        st.success(f"Saved: `{path}`")
        st.download_button("⬇️ Download TXT", content,
                           f"monthly_{today}.txt", "text/plain",
                           use_container_width=True, key="dl_monthly")

st.markdown("<hr>", unsafe_allow_html=True)

# ── Data Preview ──────────────────────────────────────────────────────────────
with st.expander("👁️ Preview: All Tickets Data"):
    tickets = get_all_tickets_raw()
    if tickets:
        df = pd.DataFrame(tickets)
        show = [c for c in ["ticket_id","student_name","department","priority",
                             "status","intent","sentiment","created_at"] if c in df.columns]
        df = df[show]
        df.columns = [c.replace("_"," ").title() for c in show]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No tickets yet.")

st.markdown(f"""
<div style="background:{COLORS['card2']};border:1px solid {COLORS['border']};
    border-radius:14px;padding:1rem 1.2rem;margin-top:.8rem;">
    <div style="color:{COLORS['text']};font-weight:700;font-size:.85rem;margin-bottom:.4rem;">
        💡 Report Tips</div>
    <ul style="color:{COLORS['muted']};font-size:.8rem;line-height:1.9;
        padding-left:1.1rem;margin:0;">
        <li>CSV exports include all AI-enriched fields (intent, sentiment, summary, auto_reply)</li>
        <li>PDF reports require <code>pip install reportlab</code> — plain text fallback otherwise</li>
        <li>All generated reports are saved to the <code>reports/</code> folder automatically</li>
        <li>Use the Analytics page for interactive charts before exporting</li>
    </ul>
</div>""", unsafe_allow_html=True)