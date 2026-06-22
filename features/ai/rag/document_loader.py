"""
Document Loader — loads all PDFs from data/rag/ using PyPDFDirectoryLoader.
Swap loader class to support DOCX, HTML, etc. in future.
"""
import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document

RAG_DIR = "data/rag"


def load_documents() -> list[Document]:
    """
    Load all PDF files from the RAG directory.

    Returns:
        List of LangChain Document objects with page content and metadata.
    """
    if not os.path.exists(RAG_DIR):
        raise FileNotFoundError(f"RAG directory not found: {RAG_DIR}")

    loader = PyPDFDirectoryLoader(RAG_DIR)
    docs = loader.load()
    return docs
