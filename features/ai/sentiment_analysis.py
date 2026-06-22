"""
Sentiment Analyser — TF-IDF + Logistic Regression.
To swap in BERT/Transformer: replace train/predict internals only.
"""
import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

_MODEL_PATH = "models/sentiment_model/model.pkl"
_DATA_PATH  = "data/training/sentiments.csv"
_pipeline: Pipeline | None = None


def _model_path() -> str:
    os.makedirs(os.path.dirname(_MODEL_PATH), exist_ok=True)
    return _MODEL_PATH


def train_sentiment_model() -> dict:
    """Train and persist the sentiment classification pipeline."""
    df = pd.read_csv(_DATA_PATH)
    df.dropna(subset=["query", "sentiment"], inplace=True)

    X_tr, X_te, y_tr, y_te = train_test_split(
        df["query"], df["sentiment"], test_size=0.2, random_state=42, stratify=df["sentiment"]
    )
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=8_000, sublinear_tf=True)),
        ("clf",   LogisticRegression(max_iter=500, C=3.0, random_state=42)),
    ])
    pipe.fit(X_tr, y_tr)
    acc = pipe.score(X_te, y_te)
    joblib.dump(pipe, _model_path())
    return {"accuracy": round(acc, 4), "samples": len(df)}


def _load() -> Pipeline:
    global _pipeline
    if _pipeline is None:
        if not os.path.exists(_MODEL_PATH):
            train_sentiment_model()
        _pipeline = joblib.load(_MODEL_PATH)
    return _pipeline


def predict_sentiment(query: str) -> str:
    """Return predicted sentiment: Positive, Neutral, or Negative."""
    return _load().predict([query])[0]
