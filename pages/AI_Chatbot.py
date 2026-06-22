import streamlit as st
from html import escape
from core.config import APP_ICON
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from styles.custom_css import inject_css
from styles.theme import COLORS
from features.ai.chatbot.chatbot import chat, get_history, clear_history

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
inject_css()
initialize_database()
render_sidebar()

SUGGESTED = [
    "What is the minimum attendance requirement?",
    "What is the hostel curfew time?",
    "How much is the B.Tech CSE fee?",
    "What are the scholarship eligibility criteria?",
    "When do end-semester exams begin?",
    "What are the transport fees?",
    "What is the supplementary exam fee?",
    "How many room changes are allowed?",
]

# Pre-assign tokens
_c_text    = COLORS["text"]
_c_muted   = COLORS["muted"]
_c_card    = COLORS["card"]
_c_card2   = COLORS["card2"]
_c_border  = COLORS["border"]
_c_bs      = COLORS["border_solid"]
_c_bg      = COLORS["bg"]
_c_primary = COLORS["primary"]
_c_accent  = COLORS["accent"]
_c_green   = COLORS["green"]
_c_red     = COLORS["red"]

# ── Header ────────────────────────────────────────────────────────────────────
hc, bc = st.columns([6, 1])
with hc:
    page_header("💬 AI University Chatbot",
                "Ask anything about university policies, fees, exams, hostel and more.")
with bc:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear", use_container_width=True):
        clear_history()
        st.rerun()

# ── Status banner ─────────────────────────────────────────────────────────────
history = get_history()
has_quota_err = any(
    msg.get("error") and "quota" in msg.get("content", "").lower()
    for msg in history if msg.get("role") == "assistant"
)
if has_quota_err:
    st.warning(
        "⚠️ **Gemini API quota reached.** Free tier allows 20 requests/day "
        "for gemini-2.5-flash. Quota resets every 24 hours. "
        "You can still browse the Knowledge Base which searches documents directly.",
        icon="⚠️",
    )

# ── Suggested prompts ─────────────────────────────────────────────────────────
if not history:
    st.markdown(f"""
<div style="background:linear-gradient(145deg,{_c_card},{_c_card2});
    border:1px solid {_c_border};border-radius:16px;
    padding:1.2rem;margin-bottom:1rem;">
    <div style="color:{_c_muted};font-size:.72rem;font-weight:700;
        text-transform:uppercase;letter-spacing:.07em;margin-bottom:.7rem;">
        💡 Suggested Questions</div>""", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, q in enumerate(SUGGESTED):
        with cols[i % 4]:
            if st.button(q, key=f"sug_{i}", use_container_width=True):
                with st.spinner("🤖 Searching university documents…"):
                    chat(q)
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ── Chat messages ─────────────────────────────────────────────────────────────
for msg in get_history():
    if msg["role"] == "user":
        # FIX: escape user content — raw HTML in chat bubbles was the XSS/display bug
        safe_content = escape(msg["content"]).replace("\n", "<br>")
        st.markdown(f"""
<div style="display:flex;justify-content:flex-end;margin-bottom:.7rem;">
    <div style="background:linear-gradient(135deg,{_c_primary},{_c_accent});
        color:#fff;border-radius:18px 18px 4px 18px;padding:.75rem 1.1rem;
        max-width:70%;font-size:.9rem;line-height:1.5;">
        {safe_content}
    </div>
</div>""", unsafe_allow_html=True)
    else:
        is_error     = msg.get("error", False)
        bubble_bg    = _c_red + "33" if is_error else f"linear-gradient(145deg,{_c_card},{_c_card2})"
        border_color = _c_red if is_error else _c_border
        # FIX: escape assistant content too (may contain angle brackets from model output)
        safe_content = escape(msg["content"]).replace("\n", "<br>")
        st.markdown(f"""
<div style="display:flex;justify-content:flex-start;margin-bottom:.4rem;
    gap:.6rem;align-items:flex-end;">
    <div style="background:{_c_accent}33;border:1px solid {_c_accent}55;
        border-radius:50%;width:30px;height:30px;flex-shrink:0;
        display:flex;align-items:center;justify-content:center;font-size:.9rem;">
        {'⚠️' if is_error else '🤖'}
    </div>
    <div style="background:{bubble_bg};
        color:{_c_text};border:1px solid {border_color};
        border-radius:18px 18px 18px 4px;padding:.75rem 1.1rem;
        max-width:75%;font-size:.9rem;line-height:1.6;">
        {safe_content}
    </div>
</div>""", unsafe_allow_html=True)

        sources = msg.get("sources", [])
        if sources and not is_error:
            with st.expander("📄 Source Documents"):
                seen: set[str] = set()
                for doc in sources:
                    fname = (doc.metadata.get("source", "")
                             .replace("data\\rag\\", "").replace("data/rag/", ""))
                    if fname not in seen:
                        seen.add(fname)
                        st.markdown(f"""
<div style="background:{_c_bg};border:1px solid {_c_bs};
    border-radius:10px;padding:.55rem .9rem;margin-bottom:.4rem;">
    <span style="color:{_c_primary};font-weight:600;font-size:.78rem;">
        📑 {escape(fname)}</span>
    <div style="color:{_c_muted};font-size:.76rem;margin-top:.2rem;">
        {escape(doc.page_content[:280])}{'…' if len(doc.page_content) > 280 else ''}
    </div>
</div>""", unsafe_allow_html=True)

# ── Input bar ─────────────────────────────────────────────────────────────────
st.markdown(
    f"<div style='height:1px;background:{_c_bs};margin:.8rem 0;'></div>",
    unsafe_allow_html=True,
)
ic, sc = st.columns([8, 1])
with ic:
    user_input = st.text_input(
        "Message", key="chat_input",
        label_visibility="collapsed",
        placeholder="Ask a question about university policies…",
    )
with sc:
    send = st.button("Send ➤", use_container_width=True)

if send and user_input.strip():
    with st.spinner("🤖 Searching and generating answer…"):
        try:
            chat(user_input.strip())
        except Exception as e:
            st.error(f"Chat error: {e}")
    st.rerun()