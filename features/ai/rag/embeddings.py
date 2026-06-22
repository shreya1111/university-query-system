"""
Embeddings — HuggingFace sentence-transformers wrapper.
Only sets HF_HUB_OFFLINE after confirming the model is cached locally,
so the first-run download still works normally.
"""
import os
from pathlib import Path
from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# FIX: only go offline if the model cache actually exists.
# Forcing HF_HUB_OFFLINE=1 on first run causes a crash because
# there's nothing to load from cache yet.
_HF_CACHE    = Path.home() / ".cache" / "huggingface" / "hub"
_MODEL_CACHE = _HF_CACHE / ("models--" + EMBED_MODEL.replace("/", "--"))

if _MODEL_CACHE.exists():
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")


@lru_cache(maxsize=1)
def get_embedding_model() -> HuggingFaceEmbeddings:
    """Load and cache the HuggingFace embedding model."""
    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )