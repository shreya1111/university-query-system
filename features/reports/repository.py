"""
Repository layer for reports module.
Handles data retrieval for report generation.
"""
from typing import Optional, Union, List
from core.database import get_tickets_filtered


def get_tickets_for_reports(
    department: Optional[Union[str, List[str]]] = None,
    priority: Optional[Union[str, List[str]]] = None,
    status: Optional[Union[str, List[str]]] = None,
    sentiment: Optional[Union[str, List[str]]] = None,
    intent: Optional[Union[str, List[str]]] = None,
) -> list[dict]:
    """
    Fetch tickets based on the provided filters for report generation.
    :param department: Department filter (string or list of strings)
    :param priority: Priority filter (string or list of strings)
    :param status: Status filter (string or list of strings)
    :param sentiment: Sentiment filter (string or list of strings)
    :param intent: Intent filter (string or list of strings)
    :return: List of ticket dictionaries
    """
    # Use the existing get_tickets_filtered function from the database layer
    # We don't need search parameters for reports, so we pass None for those
    return get_tickets_filtered(
        department=department,
        priority=priority,
        status=status,
        sentiment=sentiment,
        intent=intent,
        search_ticket_id=None,
        search_student_name=None,
    )