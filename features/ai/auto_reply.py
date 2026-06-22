"""
Auto Reply generator — rule-based templates per department + sentiment.
Swap generate_auto_reply() with an LLM call when ready.
"""

_REPLIES: dict[str, str] = {
    "Admission Department": (
        "Thank you for reaching out. Your query regarding admissions has been received "
        "and forwarded to the Admission Department. Our team will review your application "
        "and respond within 2–3 working days."
    ),
    "Examination Department": (
        "Your query has been forwarded to the Examination Department. "
        "Please ensure you carry your valid ID proof to the exam hall. "
        "For urgent admit card issues, visit the exam section directly."
    ),
    "Hostel Department": (
        "Thank you for your feedback. Your complaint has been logged and forwarded "
        "to the Hostel Department. Maintenance or administrative issues are typically "
        "resolved within 48 hours."
    ),
    "Finance Department": (
        "Your fee-related query has been received and escalated to the Finance Department. "
        "Please keep your payment transaction ID handy. "
        "Refund or reconciliation requests are processed within 5–10 working days."
    ),
    "Placement Cell": (
        "Thank you for your interest in placement opportunities. Your query has been "
        "forwarded to the Placement Cell. Ensure your placement portal profile is complete "
        "and updated for upcoming drives."
    ),
    "Scholarship Cell": (
        "Your scholarship-related query has been received and forwarded to the Scholarship Cell. "
        "Please ensure all required documents are submitted. "
        "Processing typically takes 10–15 working days after document verification."
    ),
    "Student Affairs": (
        "Your grievance has been received and escalated to the Student Affairs Office. "
        "We take all complaints seriously. A representative will contact you within 2 working days. "
        "For urgent matters, please visit the Student Affairs Office directly."
    ),
    "Help Desk": (
        "Thank you for contacting us. Your query has been logged and forwarded to the Help Desk. "
        "A support representative will get back to you within 1–2 working days."
    ),
}

_SENTIMENT_PREFIX: dict[str, str] = {
    "Negative": "We sincerely apologise for the inconvenience caused. ",
    "Positive": "We are glad to hear from you. ",
    "Neutral":  "",
}


def generate_auto_reply(query: str, department: str, sentiment: str = "Neutral") -> str:
    """
    Generate a professional auto-reply based on department and sentiment.

    Args:
        query:      Raw student query (reserved for future LLM use).
        department: Routed department name.
        sentiment:  Predicted sentiment label.

    Returns:
        Auto-reply string.
    """
    prefix = _SENTIMENT_PREFIX.get(sentiment, "")
    body   = _REPLIES.get(department, _REPLIES["Help Desk"])
    return prefix + body
