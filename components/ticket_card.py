import streamlit as st
from core.config import THEME, PRIORITY_COLORS, STATUS_COLORS


def ticket_card(ticket: dict, show_actions: bool = False, service=None) -> None:
    pri_color = PRIORITY_COLORS.get(ticket.get("priority", "Low"), THEME["muted"])
    sta_color = STATUS_COLORS.get(ticket.get("status", "Pending"), THEME["muted"])

    st.markdown(f"""
    <div style="
        background:{THEME['secondary_bg']};
        border:1px solid {THEME['border']};
        border-radius:10px;
        padding:1rem 1.2rem;
        margin-bottom:.8rem;
    ">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.4rem;">
            <span style="color:{THEME['primary']};font-weight:700;font-size:1rem;">
                🎫 Ticket #{ticket.get('ticket_id')}
            </span>
            <div style="display:flex;gap:.5rem;">
                <span style="background:{pri_color}22;color:{pri_color};border:1px solid {pri_color};
                    padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600;">
                    ⚡ {ticket.get('priority')}
                </span>
                <span style="background:{sta_color}22;color:{sta_color};border:1px solid {sta_color};
                    padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600;">
                    {ticket.get('status')}
                </span>
            </div>
        </div>
        <div style="color:{THEME['text']};font-size:.95rem;margin:.5rem 0 .3rem;">
            👤 <strong>{ticket.get('student_name')}</strong> &nbsp;|&nbsp;
            🏢 {ticket.get('department')} &nbsp;|&nbsp;
            🕐 {str(ticket.get('created_at', ''))[:16]}
        </div>
        <div style="color:{THEME['muted']};font-size:.88rem;">
            {str(ticket.get('query',''))[:200]}{'…' if len(str(ticket.get('query',''))) > 200 else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if show_actions and service:
        with st.expander(f"⚙️  Manage Ticket #{ticket.get('ticket_id')}"):
            from core.config import STATUSES
            new_status = st.selectbox(
                "Update Status",
                STATUSES,
                index=STATUSES.index(ticket.get("status", "Pending")),
                key=f"sel_{ticket.get('ticket_id')}",
            )
            if st.button("💾 Save Status", key=f"btn_{ticket.get('ticket_id')}"):
                service.change_status(ticket["ticket_id"], new_status)
                st.success("Status updated!")
                st.rerun()
