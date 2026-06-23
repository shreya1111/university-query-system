import streamlit as st
from core.config import APP_ICON
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from components.notification_card import notification_item
from styles.custom_css import inject_css
from styles.theme import COLORS
from features.notifications.service import (
    get_notifications,
    create_notification,
    mark_as_read,
    clear_notifications,
    unread_count,
)
from features.auth.auth_utils import require_login

st.set_page_config(page_title="Notifications", page_icon="🔔", layout="wide")
require_login()
inject_css()
initialize_database()
render_sidebar()

count = unread_count()
page_header(
    "🔔 Notification Center",
    f"{count} notification{'s' if count != 1 else ''} · All ticket events and status updates."
)

# ── Top action bar ────────────────────────────────────────────────────────────
ab1, ab2, ab3, ab4 = st.columns([3, 1, 1, 1])
with ab1:
    search = st.text_input("Search", label_visibility="collapsed",
                           placeholder="🔍 Search notifications…", key="notif_search")
with ab2:
    if st.button("✅ Mark All Read", use_container_width=True):
        mark_as_read()
        st.success("Marked as read.")
        st.rerun()
with ab3:
    if st.button("🗑️ Clear All", use_container_width=True):
        clear_notifications()
        st.success("Cleared all notifications.")
        st.rerun()
with ab4:
    if st.button("🧪 Test Notif", use_container_width=True):
        create_notification("Test notification created manually.")
        st.rerun()

st.markdown(
    f"<div style='height:1px;background:{COLORS['border_solid']};margin:.7rem 0 .9rem;'></div>",
    unsafe_allow_html=True,
)

# ── Load & filter ─────────────────────────────────────────────────────────────
notifs = get_notifications(limit=100)

if not notifs:
    st.markdown(f"""
    <div style="background:{COLORS['card']};border:1px solid {COLORS['border']};
        border-radius:16px;padding:2.5rem;text-align:center;margin-top:1rem;">
        <div>🔔</div>
        <div style="color:{COLORS['text']};font-weight:700;font-size:1rem;">
            No notifications yet</div>
        <div style="color:{COLORS['muted']};font-size:.85rem;margin-top:.3rem;">
            Notifications are generated automatically when tickets are raised or updated.
        </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

filtered = [n for n in notifs
            if not search or search.lower() in n["message"].lower()]

st.markdown(
    f"<p style='color:{COLORS['muted']};font-size:.82rem;margin-bottom:.4rem;'>"
    f"Showing <b style='color:{COLORS['text']};'>{len(filtered)}</b> of "
    f"<b style='color:{COLORS['text']};'>{len(notifs)}</b> notification(s)</p>",
    unsafe_allow_html=True,
)

if not filtered:
    st.info("No notifications match your search.")
    st.stop()

# ── Split by type ─────────────────────────────────────────────────────────────
ticket_created = [n for n in filtered if "raised"   in n["message"].lower()]
ticket_status_updated = [n for n in filtered if "updated"  in n["message"].lower()]
# For resolved, we look for status update messages that mention Resolved
ticket_resolved = [n for n in ticket_status_updated if "resolved" in n["message"].lower()]
# Update the status updated list to exclude resolved ones (optional, but we can keep them in both or separate)
# We'll keep resolved separate and status updated as non-resolved updates.
ticket_status_updated = [n for n in ticket_status_updated if "resolved" not in n["message"].lower()]

other_notifs = [n for n in filtered
                  if all(kw not in n["message"].lower()
                         for kw in ("raised","updated"))]

tab1, tab2, tab3, tab4 = st.tabs([
    f"🎫 Ticket Created ({len(ticket_created)})",
    f"🔄 Status Updated ({len(ticket_status_updated)})",
    f"✅ Ticket Resolved ({len(ticket_resolved)})",
    f"📌 All ({len(filtered)})",
])

with tab1:
    if ticket_created:
        for n in ticket_created:
            notification_item(n["message"], n.get("timestamp", ""),
                              icon="🎫", color=COLORS["primary"])
    else:
        st.info("No ticket created notifications.")

with tab2:
    if ticket_status_updated:
        for n in ticket_status_updated:
            notification_item(n["message"], n.get("timestamp", ""),
                              icon="🔄", color=COLORS["blue"])
    else:
        st.info("No status update notifications.")

with tab3:
    if ticket_resolved:
        for n in ticket_resolved:
            notification_item(n["message"], n.get("timestamp", ""),
                              icon="✅", color=COLORS["green"])
    else:
        st.info("No ticket resolved notifications.")

with tab4:
    for n in filtered:
        # pick icon based on content
        if "raised" in n["message"].lower():
            icon, color = "🎫", COLORS["primary"]
        elif "updated" in n["message"].lower():
            if "resolved" in n["message"].lower():
                icon, color = "✅", COLORS["green"]
            else:
                icon, color = "🔄", COLORS["blue"]
        else:
            icon, color = "📌", COLORS["muted"]
        notification_item(n["message"], n.get("timestamp", ""),
                          icon=icon, color=color)