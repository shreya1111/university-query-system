from typing import Optional
from features.ticket_management.repository import TicketRepository
from features.ai.service import analyze_query, AIResult


class TicketService:
    def __init__(self):
        self._repo = TicketRepository()

    def raise_ticket(self, student_name: str, query: str, department: str, priority: str) -> int:
        """Legacy: create ticket without AI analysis."""
        return self._repo.create(student_name, query, department, priority)

    def raise_ticket_with_ai(
        self, student_name: str, query: str
    ) -> tuple[int, AIResult]:
        """
        Analyse query with AI pipeline, then persist all fields.
        Returns (ticket_id, ai_result).
        """
        ai: AIResult = analyze_query(query)
        tid = self._repo.create_with_ai(
            student_name=student_name,
            query=query,
            department=ai["department"],
            priority=ai["priority"],
            intent=ai["intent"],
            summary=ai["summary"],
            sentiment=ai["sentiment"],
            auto_reply=ai["auto_reply"],
        )
        return tid, ai

    def list_tickets(self, department=None, priority=None, status=None) -> list[dict]:
        return self._repo.get_all(department=department, priority=priority, status=status)

    def get_ticket(self, ticket_id: int) -> Optional[dict]:
        return self._repo.get_by_id(ticket_id)

    def change_status(self, ticket_id: int, status: str) -> None:
        self._repo.update_status(ticket_id, status)

    def dashboard_stats(self) -> dict:
        return self._repo.stats()

    def dept_chart_data(self) -> list[dict]:
        return self._repo.dept_distribution()

    def priority_chart_data(self) -> list[dict]:
        return self._repo.priority_distribution()
