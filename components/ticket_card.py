"""
ticket_card.py — renders one ticket as a styled card.

IMPORTANT: query text is NEVER rendered as HTML. It is always displayed
via st.markdown with html.escape() or via native Streamlit text functions
so that HTML tags stored in old rows appear as literal text, not markup.
"""
import re
import streamlit as st
from html import escape
from styles.theme import COLORS, PRIORITY_COLORS, STATUS_COLORS, SENTIMENT_COLORS


def _strip_html(text: str) -> str:
    """Remove any HTML tags from a string (defensive, in case DB has old dirty data)."""
    return re.sub(r"<[^>]+>", "", str(text)).strip()


def _badge(label: str, color: str) -> str:
    return (
        f'<span style="background:{color}22;color:{color};border:1px solid {color}55;'
        f'padding:2px 9px;border-radius:20px;font-size:.7rem;font-weight:700;">'
        f'{escape(str(label))}</span>'
    )


def ticket_card(ticket: dict, show_actions: bool = False, service=None) -> None:
    pri_color = PRIORITY_COLORS.get(ticket.get("priority", "Low"), COLORS["muted"])
    sta_color = STATUS_COLORS.get(ticket.get("status", "Pending"), COLORS["muted"])

    # ── Always use plain text for user-supplied content ──────────────────────
    query_plain   = _strip_html(ticket.get("query", ""))
    student_plain = escape(_strip_html(ticket.get("student_name", "—")))
    dept_plain    = escape(_strip_html(ticket.get("department", "—")))
    created_plain = escape(str(ticket.get("created_at", ""))[:16])
    ticket_id     = ticket.get("ticket_id", "")

    # compact AI row (AI-generated fields are escaped too)
    ai_parts = []
    if ticket.get("intent"):
        ai_parts.append(
            f'🎯 <strong style="color:{COLORS["text"]};">'
            f'{escape(_strip_html(ticket["intent"]))}</strong>'
        )
    if ticket.get("sentiment"):
        sc = SENTIMENT_COLORS.get(ticket["sentiment"], COLORS["muted"])
        si = {"Positive": "😊", "Neutral": "😐", "Negative": "😟"}.get(ticket["sentiment"], "")
        ai_parts.append(
            f'{si} <span style="color:{sc};">'
            f'{escape(_strip_html(ticket["sentiment"]))}</span>'
        )
    if ticket.get("summary"):
        ai_parts.append(
            f'<em style="color:{COLORS["muted"]};">'
            f'{escape(_strip_html(ticket["summary"]))}</em>'
        )
    ai_row = " &nbsp;|&nbsp; ".join(ai_parts) if ai_parts else ""

    # ── Card header (metadata only — no user text in HTML) ───────────────────
    st.markdown(f"""
<div style="background:linear-gradient(145deg,{COLORS['card']},{COLORS['card2']});
    border:1px solid {COLORS['border']};border-left:3px solid {pri_color};
    border-radius:16px;padding:1rem 1.2rem .6rem;margin-bottom:.2rem;">
    <div style="display:flex;justify-content:space-between;
        align-items:center;flex-wrap:wrap;gap:.4rem;">
        <span style="color:{COLORS['primary']};font-weight:700;font-size:.95rem;">
            🎫 Ticket #{escape(str(ticket_id))}</span>
        <div style="display:flex;gap:.4rem;flex-wrap:wrap;align-items:center;">
            {_badge(f"⚡ {ticket.get('priority','')}", pri_color)}
            {_badge(ticket.get('status',''), sta_color)}
        </div>
    </div>
    <div style="color:{COLORS['text']};font-size:.88rem;margin:.4rem 0 .15rem;">
        👤 <strong>{student_plain}</strong> &nbsp;|&nbsp;
        🏢 {dept_plain} &nbsp;|&nbsp;
        🕐 {created_plain}
    </div>
    {'<div style="font-size:.78rem;margin-bottom:.3rem;">' + ai_row + '</div>' if ai_row else ''}
</div>""", unsafe_allow_html=True)

    # ── Query text rendered as PLAIN TEXT via st.markdown with escaped content
    # We use a wrapper div only for styling; the content is html.escape()'d so
    # any HTML stored in the DB displays as literal characters, not rendered markup.
    truncated = query_plain[:220]
    ellipsis  = "…" if len(query_plain) > 220 else ""
    st.markdown(
        f'<div style="background:linear-gradient(145deg,{COLORS["card"]},{COLORS["card2"]});'
        f'border:1px solid {COLORS["border"]};border-left:3px solid {pri_color};'
        f'border-top:none;border-radius:0 0 16px 16px;'
        f'padding:.5rem 1.2rem .8rem;margin-bottom:.7rem;">'
        f'<span style="color:{COLORS["muted"]};font-size:.85rem;line-height:1.5;">'
        f'{escape(truncated)}{ellipsis}</span></div>',
        unsafe_allow_html=True,
    )

    # ── AI details expander ───────────────────────────────────────────────────
    if any(ticket.get(k) for k in ("intent", "summary", "sentiment", "auto_reply")):
        with st.expander(f"🤖 AI Details — #{escape(str(ticket_id))}"):
            a1, a2, a3 = st.columns(3)
            with a1:
                st.markdown("**Intent**")
                st.markdown(
                    f"<span style='color:{COLORS['primary']};font-weight:600;'>"
                    f"{escape(_strip_html(ticket.get('intent','—')))}</span>",
                    unsafe_allow_html=True,
                )
            with a2:
                sc = SENTIMENT_COLORS.get(ticket.get("sentiment", ""), COLORS["muted"])
                st.markdown("**Sentiment**")
                st.markdown(
                    f"<span style='color:{sc};font-weight:600;'>"
                    f"{escape(_strip_html(ticket.get('sentiment','—')))}</span>",
                    unsafe_allow_html=True,
                )
            with a3:
                st.markdown("**Summary**")
                # Plain text — no HTML rendering
                st.markdown(
                    f"<span style='color:{COLORS['muted']};'>"
                    f"{escape(_strip_html(ticket.get('summary','—')))}</span>",
                    unsafe_allow_html=True,
                )
            if ticket.get("auto_reply"):
                st.markdown("**Auto Reply**")
                safe_reply = escape(_strip_html(ticket["auto_reply"])).replace("\n", "<br>")
                st.markdown(
                    f'<div style="background:{COLORS["bg"]};border-radius:8px;'
                    f'padding:.6rem .9rem;color:{COLORS["text"]};font-size:.86rem;'
                    f'line-height:1.5;border:1px solid {COLORS["border_solid"]};">'
                    f'{safe_reply}</div>',
                    unsafe_allow_html=True,
                )

    # ── Faculty actions expander ──────────────────────────────────────────────
    if show_actions and service:
        with st.expander(f"⚙️ Manage Ticket #{escape(str(ticket_id))}"):
            from core.config import STATUSES
            cur = ticket.get("status", "Pending")
            idx = STATUSES.index(cur) if cur in STATUSES else 0
            new_status = st.selectbox(
                "Update Status", STATUSES, index=idx,
                key=f"sel_{ticket_id}",
            )
            if st.button("💾 Save", key=f"btn_{ticket_id}"):
                service.change_status(ticket["ticket_id"], new_status)
                st.success("Status updated!")
                st.rerun()