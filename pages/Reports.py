import streamlit as st
import pandas as pd
from datetime import datetime
from core.config import APP_ICON
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from styles.custom_css import inject_css
from styles.theme import COLORS
from features.reports.service import (
    generate_csv_report,
    generate_excel_report,
    generate_pdf_report,
)
from typing import Optional, Union, List

st.set_page_config(page_title="Reports", page_icon="📋", layout="wide")
inject_css()
initialize_database()
render_sidebar()
page_header("📋 Reports", "Generate and download reports in CSV, Excel, and PDF formats.")

# Pre-assign token to avoid nested-quote breakage
_c_text  = COLORS["text"]
_c_muted = COLORS["muted"]

# --- Filter Section ---
st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
with st.container():
    st.markdown(
        f"<div style='color:{_c_text};font-size:.9rem;font-weight:700;"
        f"margin-bottom:.4rem;'>🔍 Filters</div>",
        unsafe_allow_html=True,
    )
    f1, f2, f3, f4, f5 = st.columns(5)

    # Initialize filter state in session state if not present
    if "report_dept_filter" not in st.session_state:
        st.session_state.report_dept_filter = []
    if "report_pri_filter" not in st.session_state:
        st.session_state.report_pri_filter = []
    if "report_status_filter" not in st.session_state:
        st.session_state.report_status_filter = []
    if "report_sentiment_filter" not in st.session_state:
        st.session_state.report_sentiment_filter = []
    if "report_intent_filter" not in st.session_state:
        st.session_state.report_intent_filter = []

    # We need to get the filter options from the database (all tickets) to populate the multiselect
    # We can use the existing get_all_tickets function from core.database for this purpose
    from core.database import get_all_tickets
    all_tickets = get_all_tickets()  # no filters
    dept_options = sorted({t.get("department", "Unknown") for t in all_tickets if t.get("department")})
    pri_options = sorted({t.get("priority", "Unknown") for t in all_tickets if t.get("priority")})
    status_options = sorted({t.get("status", "Unknown") for t in all_tickets if t.get("status")})
    sentiment_options = sorted({t.get("sentiment", "Unknown") for t in all_tickets if t.get("sentiment")})
    intent_options = sorted({t.get("intent", "Unknown") for t in all_tickets if t.get("intent")})

    with f1:
        selected_depts = st.multiselect(
            "Department",
            options=dept_options,
            default=st.session_state.report_dept_filter,
            key="report_dept_multiselect",
        )
        st.session_state.report_dept_filter = selected_depts
    with f2:
        selected_pris = st.multiselect(
            "Priority",
            options=pri_options,
            default=st.session_state.report_pri_filter,
            key="report_pri_multiselect",
        )
        st.session_state.report_pri_filter = selected_pris
    with f3:
        selected_statuses = st.multiselect(
            "Status",
            options=status_options,
            default=st.session_state.report_status_filter,
            key="report_status_multiselect",
        )
        st.session_state.report_status_filter = selected_statuses
    with f4:
        selected_sentiments = st.multiselect(
            "Sentiment",
            options=sentiment_options,
            default=st.session_state.report_sentiment_filter,
            key="report_sentiment_multiselect",
        )
        st.session_state.report_sentiment_filter = selected_sentiments
    with f5:
        selected_intents = st.multiselect(
            "Intent",
            options=intent_options,
            default=st.session_state.report_intent_filter,
            key="report_intent_multiselect",
        )
        st.session_state.report_intent_filter = selected_intents

# Fetch filtered tickets based on selected filters
dept_filter = st.session_state.report_dept_filter if st.session_state.report_dept_filter else None
pri_filter = st.session_state.report_pri_filter if st.session_state.report_pri_filter else None
status_filter = st.session_state.report_status_filter if st.session_state.report_status_filter else None
sentiment_filter = st.session_state.report_sentiment_filter if st.session_state.report_sentiment_filter else None
intent_filter = st.session_state.report_intent_filter if st.session_state.report_intent_filter else None

# We don't have a direct function to get the count without fetching the data, but we can fetch the data and then get the length.
# However, for large datasets, this might be inefficient. But for the purpose of this task, we'll fetch the data to get the count.
# We'll use the repository function to get the tickets for the filters (without search) to display the count.
from features.reports.repository import get_tickets_for_reports
filtered_tickets = get_tickets_for_reports(
    department=dept_filter,
    priority=pri_filter,
    status=status_filter,
    sentiment=sentiment_filter,
    intent=intent_filter,
)
ticket_count = len(filtered_tickets)

st.markdown(f"<p style='color:{_c_muted};font-size:.85rem;margin-top:.5rem;'>"
            f"Found <b style='color:{_c_text};'>{ticket_count}</b> ticket{'s' if ticket_count != 1 else ''} matching the filters.</p>",
            unsafe_allow_html=True)

# --- Download Buttons ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"<div style='color:{_c_text};font-size:.95rem;font-weight:700;"
            f"margin-bottom:.8rem;'>📥 Download Reports</div>", unsafe_allow_html=True)

dl1, dl2, dl3 = st.columns(3)

with dl1:
    if st.button("Generate CSV", use_container_width=True, key="btn_csv"):
        with st.spinner("Generating CSV report..."):
            csv_bytes = generate_csv_report(
                department=dept_filter,
                priority=pri_filter,
                status=status_filter,
                sentiment=sentiment_filter,
                intent=intent_filter,
            )
        st.session_state.csv_report = csv_bytes
        st.success("CSV report generated!")
    if "csv_report" in st.session_state:
        st.download_button(
            label="⬇️ Download CSV",
            data=st.session_state.csv_report,
            file_name=f"tickets_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            key="dl_csv"
        )

with dl2:
    if st.button("Generate Excel", use_container_width=True, key="btn_excel"):
        with st.spinner("Generating Excel report..."):
            excel_bytes = generate_excel_report(
                department=dept_filter,
                priority=pri_filter,
                status=status_filter,
                sentiment=sentiment_filter,
                intent=intent_filter,
            )
        st.session_state.excel_report = excel_bytes
        st.success("Excel report generated!")
    if "excel_report" in st.session_state:
        st.download_button(
            label="⬇️ Download Excel",
            data=st.session_state.excel_report,
            file_name=f"tickets_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="dl_excel"
        )

with dl3:
    if st.button("Generate PDF", use_container_width=True, key="btn_pdf"):
        with st.spinner("Generating PDF report..."):
            pdf_bytes = generate_pdf_report(
                department=dept_filter,
                priority=pri_filter,
                status=status_filter,
                sentiment=sentiment_filter,
                intent=intent_filter,
            )
        st.session_state.pdf_report = pdf_bytes
        st.success("PDF report generated!")
    if "pdf_report" in st.session_state:
        st.download_button(
            label="⬇️ Download PDF",
            data=st.session_state.pdf_report,
            file_name=f"tickets_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="dl_pdf"
        )

# --- Optional: Data Preview ---
with st.expander("👁️ Preview: Filtered Tickets Data"):
    if filtered_tickets:
        df = pd.DataFrame(filtered_tickets)
        show = [c for c in ["ticket_id","student_name","department","priority",
                             "status","intent","sentiment","created_at"] if c in df.columns]
        df = df[show]
        df.columns = [c.replace("_"," ").title() for c in show]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No tickets match the current filters.")

st.markdown(f"""<div style="background:{COLORS['card2']};border:1px solid {COLORS['border']};
    border-radius:14px;padding:1rem 1.2rem;margin-top:.8rem;">
    <div style="color:{COLORS['text']};font-weight:700;font-size:.85rem;margin-bottom:.4rem;">
        💡 Report Tips</div>
    <ul style="color:{COLORS['muted']};font-size:.8rem;line-height:1.9;
        padding-left:1.1rem;margin:0;">
        <li>Select filters to include only specific tickets in the report.</li>
        <li>If no filters are selected, the report will include all tickets.</li>
        <li>Click the 'Generate' button for each format before downloading.</li>
        <li>Reports are generated dynamically and not saved to the server.</li>
    </ul>
</div>""", unsafe_allow_html=True)