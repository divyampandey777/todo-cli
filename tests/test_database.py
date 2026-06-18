"""Tests for todo_cli.database using a temporary SQLite file per test."""
import tempfile
from pathlib import Path

import pytest

from todo_cli.database import TaskDatabase
from todo_cli.models import Task


@pytest.fixture
def db():
    with tempfile.TemporaryDirectory() as tmp:
        database = TaskDatabase(db_path=Path(tmp) / "test.db")
        yield database
        database.close()


def test_add_and_get_task(db):
    task = Task(id=None, title="Buy milk", priority="low")
    task_id = db.add(task)

    fetched = db.get(task_id)
    assert fetched is not None
    assert fetched.title == "Buy milk"
    assert fetched.priority == "low"
    assert fetched.done is False


def test_list_all_excludes_done_by_default(db):
    id1 = db.add(Task(id=None, title="Task A"))
    db.add(Task(id=None, title="Task B"))
    db.mark_done(id1)

    pending = db.list_all(show_done=False)
    assert len(pending) == 1
    assert pending[0].title == "Task B"

    everything = db.list_all(show_done=True)
    assert len(everything) == 2


def test_filter_by_category(db):
    db.add(Task(id=None, title="Work task", category="work"))
    db.add(Task(id=None, title="Home task", category="home"))

    results = db.list_all(category="work")
    assert len(results) == 1
    assert results[0].title == "Work task"


def test_filter_by_priority(db):
    db.add(Task(id=None, title="Urgent", priority="high"))
    db.add(Task(id=None, title="Chill", priority="low"))

    results = db.list_all(priority="high")
    assert len(results) == 1
    assert results[0].title == "Urgent"


def test_search_by_title(db):
    db.add(Task(id=None, title="Finish report"))
    db.add(Task(id=None, title="Walk the dog"))

    results = db.list_all(search="report")
    assert len(results) == 1
    assert results[0].title == "Finish report"


def test_mark_done(db):
    task_id = db.add(Task(id=None, title="Do laundry"))
    assert db.mark_done(task_id) is True

    task = db.get(task_id)
    assert task.done is True

    assert db.mark_done(9999) is False


def test_delete(db):
    task_id = db.add(Task(id=None, title="Temp task"))
    assert db.delete(task_id) is True
    assert db.get(task_id) is None
    assert db.delete(task_id) is False


def test_invalid_priority_raises():
    with pytest.raises(ValueError):
        Task(id=None, title="Bad priority", priority="urgent")


def test_invalid_due_date_raises():
    with pytest.raises(ValueError):
        Task(id=None, title="Bad date", due_date="not-a-date")


def test_overdue_detection():
    overdue_task = Task(id=None, title="Old task", due_date="2000-01-01")
    assert overdue_task.is_overdue is True

    future_task = Task(id=None, title="Future task", due_date="2999-01-01")
    assert future_task.is_overdue is False

    done_overdue_task = Task(
        id=None, title="Done but overdue", due_date="2000-01-01", done=True
    )
    assert done_overdue_task.is_overdue is False
