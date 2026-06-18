"""SQLite persistence layer for tasks."""
import sqlite3
from pathlib import Path
from typing import List, Optional

from todo_cli.models import Task

DEFAULT_DB_PATH = Path.home() / ".todo_cli" / "todo.db"


class TaskDatabase:
    """Handles all SQLite interactions for tasks."""

    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                priority TEXT NOT NULL DEFAULT 'medium',
                due_date TEXT,
                category TEXT
            )
            """
        )
        self._conn.commit()

    def add(self, task: Task) -> int:
        cursor = self._conn.execute(
            """
            INSERT INTO tasks (title, done, priority, due_date, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            (task.title, int(task.done), task.priority, task.due_date, task.category),
        )
        self._conn.commit()
        return cursor.lastrowid

    def get(self, task_id: int) -> Optional[Task]:
        row = self._conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return self._row_to_task(row) if row else None

    def list_all(
        self,
        show_done: bool = True,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Task]:
        query = "SELECT * FROM tasks WHERE 1=1"
        params: list = []

        if not show_done:
            query += " AND done = 0"
        if category:
            query += " AND category = ?"
            params.append(category)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        if search:
            query += " AND title LIKE ?"
            params.append(f"%{search}%")

        query += " ORDER BY done ASC, due_date IS NULL, due_date ASC, id ASC"

        rows = self._conn.execute(query, params).fetchall()
        return [self._row_to_task(row) for row in rows]

    def mark_done(self, task_id: int) -> bool:
        cursor = self._conn.execute(
            "UPDATE tasks SET done = 1 WHERE id = ?", (task_id,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def delete(self, task_id: int) -> bool:
        cursor = self._conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self._conn.commit()
        return cursor.rowcount > 0

    def close(self) -> None:
        self._conn.close()

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> Task:
        return Task(
            id=row["id"],
            title=row["title"],
            done=bool(row["done"]),
            priority=row["priority"],
            due_date=row["due_date"],
            category=row["category"],
        )
