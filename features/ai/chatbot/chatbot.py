"""
Chatbot — wraps RAG engine with session-state conversation history.
All errors are caught and stored as assistant messages (never crash the UI).
"""
import streamlit as st
from features.ai.rag.rag_engine import query_rag

HISTORY_KEY = "chat_history"

_QUOTA_MSG = (
    "⚠️ The SambaNova API quota or rate limit has been reached. "
    "Please wait a moment and try again, or check your API key at "
    "https://cloud.sambanova.ai"
)

_ERROR_MSG = (
    "I encountered an error while processing your question. "
    "Please try again in a moment."
)


def _init_history() -> None:
    if HISTORY_KEY not in st.session_state:
        st.session_state[HISTORY_KEY] = []


def chat(query: str) -> dict:
    """
    Send a query through the RAG pipeline and store in session history.
    Errors are caught and stored as assistant error messages.
    """
    _init_history()

    # Store user message immediately
    st.session_state[HISTORY_KEY].append({
        "role":    "user",
        "content": query,
        "error":   False,
    })

    try:
        result = query_rag(query)
        st.session_state[HISTORY_KEY].append({
            "role":    "assistant",
            "content": result["answer"],
            "sources": result["source_documents"],
            "error":   False,
        })
        return result

    except RuntimeError as e:
        err_str = str(e).lower()
        if "quota" in err_str or "rate" in err_str or "limit" in err_str:
            msg = _QUOTA_MSG
        else:
            msg = str(e)
        st.session_state[HISTORY_KEY].append({
            "role":    "assistant",
            "content": msg,
            "sources": [],
            "error":   True,
        })
        return {"answer": msg, "source_documents": []}

    except Exception as e:
        # FIX: was unindented — ran unconditionally, overwriting good results
        error_msg = f"ERROR: {str(e)}"
        st.session_state[HISTORY_KEY].append({
            "role":    "assistant",
            "content": error_msg,
            "sources": [],
            "error":   True,
        })
        return {"answer": error_msg, "source_documents": []}


def get_history() -> list[dict]:
    _init_history()
    return st.session_state[HISTORY_KEY]


def clear_history() -> None:
    st.session_state[HISTORY_KEY] = []