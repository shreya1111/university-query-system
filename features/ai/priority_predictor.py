"""
Priority Predictor — TF-IDF + RandomForestClassifier.
To swap in a neural model: replace train/predict internals only.
"""
import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

_MODEL_PATH = "models/priority_model/model.pkl"
_DATA_PATH  = "data/training/priorities.csv"
_pipeline: Pipeline | None = None


def _model_path() -> str:
    os.makedirs(os.path.dirname(_MODEL_PATH), exist_ok=True)
    return _MODEL_PATH


def train_priority_model() -> dict:
    """Train and persist the priority prediction pipeline."""
    df = pd.read_csv(_DATA_PATH)
    df.dropna(subset=["query", "priority"], inplace=True)

    X_tr, X_te, y_tr, y_te = train_test_split(
        df["query"], df["priority"], test_size=0.2, random_state=42, stratify=df["priority"]
    )
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=8_000, sublinear_tf=True)),
        ("clf",   RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)),
    ])
    pipe.fit(X_tr, y_tr)
    acc = pipe.score(X_te, y_te)
    joblib.dump(pipe, _model_path())
    return {"accuracy": round(acc, 4), "samples": len(df)}


def _load() -> Pipeline:
    global _pipeline
    if _pipeline is None:
        if not os.path.exists(_MODEL_PATH):
            train_priority_model()
        _pipeline = joblib.load(_MODEL_PATH)
    return _pipeline


def predict_priority(query: str) -> str:
    """Return predicted priority: High, Medium, or Low."""
    return _load().predict([query])[0]
