"""
AI Service — orchestrates the full analysis pipeline.
Each step is independently swappable with ML/LLM implementations.
"""
from typing import TypedDict

from features.ai.intent_classifier  import predict_intent
from features.ai.department_router  import route_department
from features.ai.priority_predictor import predict_priority
from features.ai.summarizer         import summarize_query
from features.ai.sentiment_analysis import predict_sentiment
from features.ai.auto_reply         import generate_auto_reply


class AIResult(TypedDict):
    intent:     str
    department: str
    priority:   str
    summary:    str
    sentiment:  str
    auto_reply: str


def analyze_query(query: str) -> AIResult:
    """
    Run the full AI pipeline on a student query.

    Pipeline:
        query → intent → department → priority → summary → sentiment → auto_reply

    Args:
        query: Raw student query text.

    Returns:
        AIResult dict with all six fields populated.
    """
    intent     = predict_intent(query)
    department = route_department(intent)
    priority   = predict_priority(query)
    summary    = summarize_query(query)
    sentiment  = predict_sentiment(query)
    auto_reply = generate_auto_reply(query, department, sentiment)

    return AIResult(
        intent=intent,
        department=department,
        priority=priority,
        summary=summary,
        sentiment=sentiment,
        auto_reply=auto_reply,
    )
