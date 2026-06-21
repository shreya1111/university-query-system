from dataclasses import dataclass
from typing import Optional


@dataclass
class Ticket:
    student_name: str
    query: str
    department: str
    priority: str
    status: str = "Pending"
    ticket_id: Optional[int] = None
    created_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}
