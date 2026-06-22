"""
Rule-based summarizer.
Swap summarize_query() body with an LLM/T5 call when ready.
"""
import re

# intent keyword → short summary phrase
_SUMMARY_MAP: list[tuple[list[str], str]] = [
    (["admit card", "hall ticket"],              "Student facing admit card issue"),
    (["roll number", "roll no"],                 "Student requesting roll number details"),
    (["result", "marksheet", "grade", "marks"],  "Student enquiring about examination results"),
    (["revaluation"],                            "Student requesting revaluation of paper"),
    (["backlog"],                                "Student seeking backlog exam information"),
    (["exam form", "exam fee"],                  "Student facing exam form submission issue"),
    (["timetable", "schedule"],                  "Student requesting exam/class schedule"),
    (["fee", "challan", "payment", "refund"],    "Student reporting a fee or payment issue"),
    (["scholarship"],                            "Student facing scholarship-related issue"),
    (["hostel", "room", "mess", "warden"],       "Student reporting a hostel-related complaint"),
    (["placement", "internship", "drive"],       "Student enquiring about placement opportunities"),
    (["admission", "enroll", "seat"],            "Student enquiring about admission process"),
    (["complaint", "harassment", "ragging"],     "Student filing a complaint or grievance"),
    (["attendance"],                             "Student raising an attendance concern"),
    (["library"],                                "Student requesting library-related information"),
    (["transport", "bus"],                       "Student enquiring about transport facility"),
    (["certificate", "bonafide", "migration"],   "Student requesting official certificate"),
    (["password", "portal", "login", "wi-fi"],   "Student facing IT or portal access issue"),
    (["water", "electricity", "maintenance"],    "Student reporting infrastructure issue"),
]


def summarize_query(query: str) -> str:
    """
    Generate a concise one-line summary for a student query.

    Args:
        query: Raw student query string.

    Returns:
        One-line summary string.
    """
    lower = query.lower()
    for keywords, summary in _SUMMARY_MAP:
        if any(kw in lower for kw in keywords):
            return summary + "."

    # Generic fallback: take first meaningful sentence (≤12 words)
    sentences = re.split(r"[.!?]", query.strip())
    first = sentences[0].strip() if sentences else query.strip()
    words = first.split()
    short = " ".join(words[:12])
    if len(words) > 12:
        short += "..."
    return short.capitalize() + "." if short else "Student submitted a general query."
