"""
RAG Engine — retrieves context from ChromaDB then calls SambaNova via OpenAI-compatible API.

LLM is swappable: replace _call_llm() to use OpenAI, Groq, or LangChain.
"""
import os
import time
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.documents import Document
from features.ai.rag.retriever import retrieve_documents

# FIX: resolve .env relative to this file so it works regardless of cwd
_ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=False)
# Also try cwd fallback
load_dotenv(override=False)

# ── Model config ──────────────────────────────────────────────────────────────
LLM_MODEL       = "Meta-Llama-3.3-70B-Instruct"
MAX_RETRIES     = 2
RETRY_DELAY_SEC = 3

_FALLBACK_MSG = (
    "I could not find relevant information in the university documents. "
    "Please contact the relevant department directly."
)

_PROMPT_TEMPLATE = """\
You are a helpful university assistant.
Answer the student's question using ONLY the context provided below.
Be concise and accurate. If the answer is not present in the context, say exactly:
"I could not find relevant information in the university documents. \
Please contact the relevant department directly."

Context:
{context}

Question: {question}

Answer:"""


# FIX: RAGResult is a TypedDict — cannot be called as a constructor.
# Use plain dict literals everywhere instead.
class RAGResult(TypedDict):
    answer: str
    source_documents: list[Document]


def _format_docs(docs: list[Document]) -> str:
    return "\n\n---\n\n".join(d.page_content for d in docs)


def _call_llm(prompt: str) -> str:
    """Call SambaNova API using OpenAI-compatible interface."""
    from openai import OpenAI

    api_key = os.getenv("SAMBANOVA_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "SAMBANOVA_API_KEY is not set in .env — "
            "add it as: SAMBANOVA_API_KEY=your_key_here"
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.sambanova.ai/v1",
    )

    last_err = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1000,
            )
            answer = response.choices[0].message.content
            return answer.strip() if answer else _FALLBACK_MSG

        except Exception as e:
            last_err = e
            err_str = str(e).lower()
            # Don't retry on auth errors — they won't resolve with retries
            if any(kw in err_str for kw in ("auth", "invalid", "expired", "unauthorized")):
                raise RuntimeError(f"SambaNova API auth error: {e}") from e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SEC)
                continue

    raise RuntimeError(f"SambaNova API Error after {MAX_RETRIES+1} attempts: {last_err}")


def query_rag(question: str) -> RAGResult:
    """
    Full RAG pipeline: retrieve → format → LLM → return.

    Returns:
        RAGResult dict with 'answer' and 'source_documents'.

    Raises:
        RuntimeError: on API/quota errors with a user-readable message.
    """
    if not question.strip():
        # FIX: use dict literal, not RAGResult(...) constructor call
        return {"answer": _FALLBACK_MSG, "source_documents": []}

    source_docs = retrieve_documents(question)

    if not source_docs:
        return {"answer": _FALLBACK_MSG, "source_documents": []}

    context = _format_docs(source_docs)
    prompt  = _PROMPT_TEMPLATE.format(context=context, question=question)
    answer  = _call_llm(prompt)

    return {"answer": answer, "source_documents": source_docs}
