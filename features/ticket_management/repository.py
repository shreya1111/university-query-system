from typing import Optional
from core.database import (
    create_ticket,
    create_ticket_with_ai,
    get_all_tickets,
    get_ticket_by_id,
    update_ticket_status,
    get_stats,
    get_dept_distribution,
    get_priority_distribution,
)


class TicketRepository:
    def create(self, student_name: str, query: str, department: str, priority: str) -> int:
        return create_ticket(student_name, query, department, priority)

    def create_with_ai(
        self,
        student_name: str,
        query: str,
        department: str,
        priority: str,
        intent: str,
        summary: str,
        sentiment: str,
        auto_reply: str,
    ) -> int:
        return create_ticket_with_ai(
            student_name, query, department, priority,
            intent, summary, sentiment, auto_reply,
        )

    def get_all(self, department=None, priority=None, status=None) -> list[dict]:
        return get_all_tickets(department=department, priority=priority, status=status)

    def get_by_id(self, ticket_id: int) -> Optional[dict]:
        return get_ticket_by_id(ticket_id)

    def update_status(self, ticket_id: int, status: str) -> None:
        update_ticket_status(ticket_id, status)

    def stats(self) -> dict:
        return get_stats()

    def dept_distribution(self) -> list[dict]:
        return get_dept_distribution()

    def priority_distribution(self) -> list[dict]:
        return get_priority_distribution()
