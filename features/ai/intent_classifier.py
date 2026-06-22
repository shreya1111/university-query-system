"""
Intent Classifier — TF-IDF + Logistic Regression.
To swap in BERT/Gemini: replace train/predict internals only.
"""
import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

_MODEL_PATH = "models/intent_model/model.pkl"
_DATA_PATH  = "data/training/intents.csv"
_pipeline: Pipeline | None = None


def _model_path() -> str:
    os.makedirs(os.path.dirname(_MODEL_PATH), exist_ok=True)
    return _MODEL_PATH


def train_intent_model() -> dict:
    """Train and persist the intent classification pipeline."""
    df = pd.read_csv(_DATA_PATH)
    df.dropna(subset=["query", "intent"], inplace=True)

    X_tr, X_te, y_tr, y_te = train_test_split(
        df["query"], df["intent"], test_size=0.2, random_state=42, stratify=df["intent"]
    )
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=10_000, sublinear_tf=True)),
        ("clf",   LogisticRegression(max_iter=500, C=5.0, random_state=42)),
    ])
    pipe.fit(X_tr, y_tr)
    acc = pipe.score(X_te, y_te)
    joblib.dump(pipe, _model_path())
    return {"accuracy": round(acc, 4), "samples": len(df)}


def _load() -> Pipeline:
    global _pipeline
    if _pipeline is None:
        if not os.path.exists(_MODEL_PATH):
            train_intent_model()
        _pipeline = joblib.load(_MODEL_PATH)
    return _pipeline


def predict_intent(query: str) -> str:
    """Return the predicted intent label for a query string."""
    return _load().predict([query])[0]
