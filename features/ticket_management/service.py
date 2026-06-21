from typing import Optional
from features.ticket_management.repository import TicketRepository


class TicketService:
    def __init__(self):
        self._repo = TicketRepository()

    def raise_ticket(self, student_name: str, query: str, department: str, priority: str) -> int:
        return self._repo.create(student_name, query, department, priority)

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
