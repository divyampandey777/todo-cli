"""Data model for a Task."""
from dataclasses import dataclass
from datetime import date
from typing import Optional


VALID_PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    """Represents a single to-do item."""

    id: Optional[int]
    title: str
    done: bool = False
    priority: str = "medium"
    due_date: Optional[str] = None  # stored as ISO format string "YYYY-MM-DD"
    category: Optional[str] = None

    def __post_init__(self):
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority '{self.priority}'. Must be one of {VALID_PRIORITIES}."
            )
        if self.due_date:
            # Will raise ValueError if not a valid ISO date, which is what we want.
            date.fromisoformat(self.due_date)

    @property
    def is_overdue(self) -> bool:
        if not self.due_date or self.done:
            return False
        return date.fromisoformat(self.due_date) < date.today()

    def status_symbol(self) -> str:
        return "✔" if self.done else "✘"
