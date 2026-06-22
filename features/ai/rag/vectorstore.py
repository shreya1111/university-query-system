"""
Vector Store — ChromaDB with persistent storage.
Swap Chroma for FAISS/Pinecone/Weaviate by changing this file only.
"""
import os
from pathlib import Path
from langchain_core.documents import Document
from langchain_chroma import Chroma
from features.ai.rag.embeddings import get_embedding_model
from features.ai.rag.document_loader import load_documents
from features.ai.rag.chunker import split_documents

# FIX: use absolute path anchored to project root so Streamlit's cwd
# never causes "vectorstore not found" errors
_PROJECT_ROOT   = Path(__file__).resolve().parents[3]
CHROMA_DIR      = str(_PROJECT_ROOT / "vectorstore" / "chroma_db")
COLLECTION_NAME = "university_docs"


def build_vectorstore() -> Chroma:
    """
    Load PDFs, chunk them, embed and persist to ChromaDB.

    Returns:
        Chroma vectorstore instance.
    """
    print("[VectorStore] Loading documents…")
    docs   = load_documents()
    chunks = split_documents(docs)
    print(f"[VectorStore] {len(docs)} docs → {len(chunks)} chunks")

    os.makedirs(CHROMA_DIR, exist_ok=True)
    vs = Chroma.from_documents(
        documents=chunks,
        embedding=get_embedding_model(),
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
    )
    print("[VectorStore] Built and persisted.")
    return vs


def load_vectorstore() -> Chroma:
    """
    Load existing ChromaDB; build it first if it does not exist.

    Returns:
        Chroma vectorstore instance.
    """
    if not os.path.exists(CHROMA_DIR) or not os.listdir(CHROMA_DIR):
        return build_vectorstore()

    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=get_embedding_model(),
        collection_name=COLLECTION_NAME,
    )
