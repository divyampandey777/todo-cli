"""Command-line interface for the todo app."""
import argparse
import sys
from datetime import date

from todo_cli.database import TaskDatabase
from todo_cli.models import Task, VALID_PRIORITIES

PRIORITY_ICON = {"high": "🔴", "medium": "🟡", "low": "🟢"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple, fast CLI to-do list manager.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="Task description")
    add_p.add_argument(
        "-p", "--priority", choices=VALID_PRIORITIES, default="medium"
    )
    add_p.add_argument("-d", "--due", help="Due date (YYYY-MM-DD)")
    add_p.add_argument("-c", "--category", help="Category/tag")

    # list
    list_p = subparsers.add_parser("list", help="List tasks")
    list_p.add_argument(
        "-a", "--all", action="store_true", help="Include completed tasks"
    )
    list_p.add_argument("-c", "--category", help="Filter by category")
    list_p.add_argument("-p", "--priority", choices=VALID_PRIORITIES)
    list_p.add_argument("-s", "--search", help="Search title text")

    # done
    done_p = subparsers.add_parser("done", help="Mark a task as completed")
    done_p.add_argument("id", type=int)

    # delete
    del_p = subparsers.add_parser("delete", help="Delete a task")
    del_p.add_argument("id", type=int)

    return parser


def format_task(task: Task) -> str:
    parts = [f"[{task.id}]", task.status_symbol(), PRIORITY_ICON[task.priority], task.title]
    if task.category:
        parts.append(f"#{task.category}")
    if task.due_date:
        marker = " (OVERDUE)" if task.is_overdue else ""
        parts.append(f"due:{task.due_date}{marker}")
    return "  ".join(parts)


def run(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    db = TaskDatabase()

    try:
        if args.command == "add":
            if args.due:
                try:
                    date.fromisoformat(args.due)
                except ValueError:
                    print(f"Error: due date must be YYYY-MM-DD, got '{args.due}'")
                    return 1
            task = Task(
                id=None,
                title=args.title,
                priority=args.priority,
                due_date=args.due,
                category=args.category,
            )
            task_id = db.add(task)
            print(f"Added task [{task_id}]: {args.title}")

        elif args.command == "list":
            tasks = db.list_all(
                show_done=args.all,
                category=args.category,
                priority=args.priority,
                search=args.search,
            )
            if not tasks:
                print("No tasks found.")
            for t in tasks:
                print(format_task(t))

        elif args.command == "done":
            if db.mark_done(args.id):
                print(f"Marked task [{args.id}] as done.")
            else:
                print(f"No task with id {args.id}.")
                return 1

        elif args.command == "delete":
            if db.delete(args.id):
                print(f"Deleted task [{args.id}].")
            else:
                print(f"No task with id {args.id}.")
                return 1

    finally:
        db.close()

    return 0


def main():
    sys.exit(run())
