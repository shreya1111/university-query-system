import streamlit as st
from html import escape
from core.config import APP_ICON
from core.database import initialize_database
from components.sidebar import render_sidebar
from components.cards import page_header
from styles.custom_css import inject_css
from styles.theme import COLORS
from features.ai.rag.rag_engine import query_rag, RAGResult

st.set_page_config(page_title="Knowledge Base", page_icon="📚", layout="wide")
inject_css()
initialize_database()
render_sidebar()
page_header("📚 Knowledge Base",
            "Search university policies, regulations, fees, and FAQs.")

# Pre-assign tokens
_c_text    = COLORS["text"]
_c_muted   = COLORS["muted"]
_c_card    = COLORS["card"]
_c_card2   = COLORS["card2"]
_c_border  = COLORS["border"]
_c_bs      = COLORS["border_solid"]
_c_bg      = COLORS["bg"]
_c_primary = COLORS["primary"]

TOPICS = {
    "📅 Attendance":    "What is the minimum attendance requirement and condonation policy?",
    "💰 Fees":          "What is the complete fee structure for B.Tech students?",
    "🏠 Hostel":        "What are the hostel rules and curfew timings?",
    "🎓 Scholarships":  "What are the scholarship eligibility criteria and application process?",
    "📝 Exams":         "What are the examination rules and supplementary exam policy?",
    "🚌 Transport":     "What are the transport routes and fee structure?",
    "📖 Library":       "What are the library rules and borrowing limits?",
    "🏛️ Placement":    "What is the placement policy and eligibility criteria?",
}

# ── Quick topic buttons ───────────────────────────────────────────────────────
# FIX: original had an unclosed opening <div> — the closing </div> was missing
st.markdown(f"""
<div style="background:linear-gradient(145deg,{_c_card},{_c_card2});
    border:1px solid {_c_border};border-radius:16px;
    padding:1.2rem;margin-bottom:1rem;">
    <div style="color:{_c_muted};font-size:.7rem;font-weight:700;
        text-transform:uppercase;letter-spacing:.08em;margin-bottom:.7rem;">
        📌 Quick Topics</div>
</div>""", unsafe_allow_html=True)

tcols = st.columns(4)
for i, (label, q) in enumerate(TOPICS.items()):
    with tcols[i % 4]:
        if st.button(label, key=f"topic_{i}", use_container_width=True):
            st.session_state["kb_query"]   = q
            st.session_state["kb_trigger"] = True

# ── Search bar ────────────────────────────────────────────────────────────────
sc1, sc2 = st.columns([7, 1])
with sc1:
    search_q = st.text_input(
        "Search",
        value=st.session_state.get("kb_query", ""),
        key="kb_input",
        label_visibility="collapsed",
        placeholder="e.g. What are the hostel curfew rules?",
    )
with sc2:
    search_btn = st.button("🔍 Search", use_container_width=True)

trigger = search_btn or st.session_state.pop("kb_trigger", False)

if trigger and search_q.strip():
    st.session_state["kb_query"] = ""

    with st.spinner("🔍 Searching university knowledge base…"):
        try:
            result: RAGResult = query_rag(search_q.strip())
            error_msg = None
        except RuntimeError as e:
            result    = None
            error_msg = str(e)
        except Exception:
            result    = None
            error_msg = "An unexpected error occurred while searching. Please try again."

    if error_msg:
        if "quota" in error_msg.lower():
            st.warning(
                "⚠️ **Gemini API quota reached** — the AI answer generation is temporarily "
                "unavailable. Relevant document excerpts are shown below using direct vector search.",
                icon="⚠️",
            )
            try:
                from features.ai.rag.retriever import retrieve_documents
                docs = retrieve_documents(search_q.strip())
                if docs:
                    st.markdown(
                        f"<div style='color:{_c_text};font-size:.9rem;"
                        f"font-weight:700;margin:.8rem 0 .5rem;'>"
                        f"📑 Relevant Document Excerpts</div>",
                        unsafe_allow_html=True,
                    )
                    seen: set[str] = set()
                    for doc in docs:
                        fname = (doc.metadata.get("source", "")
                                 .replace("data\\rag\\", "").replace("data/rag/", ""))
                        page  = doc.metadata.get("page", "?")
                        seen.add(fname)
                        with st.expander(f"📑 {fname}  — page {page}"):
                            st.markdown(
                                f'<div style="background:{_c_bg};'
                                f'border-radius:10px;padding:.8rem 1rem;'
                                f'color:{_c_text};font-size:.86rem;'
                                f'line-height:1.6;white-space:pre-wrap;'
                                f'border:1px solid {_c_bs};">'
                                f'{escape(doc.page_content)}</div>',
                                unsafe_allow_html=True,
                            )
            except Exception:
                pass
        else:
            st.error(f"Error: {error_msg}")

    elif result:
        # ── Answer card ───────────────────────────────────────────────────────
        answer_safe = escape(result["answer"]).replace("\n", "<br>")
        st.markdown(f"""
<div style="background:linear-gradient(145deg,{_c_card},{_c_card2});
    border:1px solid {_c_primary}55;border-left:4px solid {_c_primary};
    border-radius:16px;padding:1.4rem;margin-top:.8rem;">
    <div style="color:{_c_muted};font-size:.68rem;font-weight:700;
        text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;">
        💡 Answer</div>
    <div style="color:{_c_text};font-size:.92rem;line-height:1.75;">
        {answer_safe}
    </div>
</div>""", unsafe_allow_html=True)

        # ── Source chunks ─────────────────────────────────────────────────────
        if result["source_documents"]:
            st.markdown("<div style='height:.8rem;'></div>", unsafe_allow_html=True)
            st.markdown(
                f"<div style='color:{_c_muted};font-size:.8rem;margin-bottom:.6rem;'>"
                f"📑 <b style='color:{_c_text};'>"
                f"{len(result['source_documents'])}</b> source chunk(s) retrieved</div>",
                unsafe_allow_html=True,
            )
            seen_files: set[str] = set()
            for doc in result["source_documents"]:
                fname = (doc.metadata.get("source", "")
                         .replace("data\\rag\\", "").replace("data/rag/", ""))
                page  = doc.metadata.get("page", "?")
                seen_files.add(fname)
                with st.expander(f"📑 {fname}  — page {page}"):
                    st.markdown(
                        f'<div style="background:{_c_bg};border-radius:10px;'
                        f'padding:.8rem 1rem;color:{_c_text};font-size:.86rem;'
                        f'line-height:1.6;white-space:pre-wrap;'
                        f'border:1px solid {_c_bs};">'
                        f'{escape(doc.page_content)}</div>',
                        unsafe_allow_html=True,
                    )

elif trigger:
    st.warning("Please enter a search query.")