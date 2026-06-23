"""
Service layer for reports module.
Handles report generation logic.
"""
import os
import pandas as pd
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Any, Optional, Union  # FIX: Optional/Union were missing here

from features.reports.repository import get_tickets_for_reports
from core.config import DB_PATH  # kept for context


def _prepare_ticket_data(tickets: List[Dict[str, Any]]) -> pd.DataFrame:
    if not tickets:
        return pd.DataFrame(columns=[
            "ticket_id", "student_name", "department", "priority",
            "status", "intent", "sentiment", "created_at",
        ])
    df = pd.DataFrame(tickets)
    required_columns = [
        "ticket_id", "student_name", "department", "priority",
        "status", "intent", "sentiment", "created_at",
    ]
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""
    return df[required_columns]


def generate_csv_report(
    department: Optional[Union[str, List[str]]] = None,
    priority:   Optional[Union[str, List[str]]] = None,
    status:     Optional[Union[str, List[str]]] = None,
    sentiment:  Optional[Union[str, List[str]]] = None,
    intent:     Optional[Union[str, List[str]]] = None,
) -> bytes:
    tickets = get_tickets_for_reports(
        department=department, priority=priority, status=status,
        sentiment=sentiment, intent=intent,
    )
    df = _prepare_ticket_data(tickets)
    return df.to_csv(index=False).encode("utf-8")


def generate_excel_report(
    department: Optional[Union[str, List[str]]] = None,
    priority:   Optional[Union[str, List[str]]] = None,
    status:     Optional[Union[str, List[str]]] = None,
    sentiment:  Optional[Union[str, List[str]]] = None,
    intent:     Optional[Union[str, List[str]]] = None,
) -> bytes:
    tickets = get_tickets_for_reports(
        department=department, priority=priority, status=status,
        sentiment=sentiment, intent=intent,
    )
    df = _prepare_ticket_data(tickets)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Tickets")
    return buffer.getvalue()


def generate_pdf_report(
    department: Optional[Union[str, List[str]]] = None,
    priority:   Optional[Union[str, List[str]]] = None,
    status:     Optional[Union[str, List[str]]] = None,
    sentiment:  Optional[Union[str, List[str]]] = None,
    intent:     Optional[Union[str, List[str]]] = None,
) -> bytes:
    tickets = get_tickets_for_reports(
        department=department, priority=priority, status=status,
        sentiment=sentiment, intent=intent,
    )
    df = _prepare_ticket_data(tickets)

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle", parent=styles["Heading1"],
        fontSize=16, spaceAfter=30, alignment=TA_CENTER,
    )
    elements.append(Paragraph("University Query System - Tickets Report", title_style))
    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles["Normal"],
    ))
    elements.append(Spacer(1, 12))

    data = [df.columns.tolist()] + [
        [str(v) for v in row] for row in df.itertuples(index=False)
    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  colors.grey),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.whitesmoke),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0),  10),
        ("BOTTOMPADDING", (0, 0), (-1, 0),  12),
        ("BACKGROUND",    (0, 1), (-1, -1), colors.beige),
        ("TEXTCOLOR",     (0, 1), (-1, -1), colors.black),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 8),
        ("GRID",          (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)
    return buffer.getvalue()