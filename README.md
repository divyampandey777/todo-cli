# todo-cli

A fast, dependency-free command-line to-do list manager built in Python, backed by SQLite.

## Features

- ✅ Add, list, complete, and delete tasks
- 🎯 Priorities (`high` / `medium` / `low`)
- 📅 Due dates with automatic overdue detection
- 🏷️ Categories/tags for organizing tasks
- 🔍 Search and filter by category, priority, or keyword
- 💾 Persistent storage via SQLite (no server, no setup)
- 🧪 Fully unit tested with `pytest`

## Installation

```bash
git clone https://github.com/<your-username>/todo-cli.git
cd todo-cli
pip install -e .
```

This installs a `todo` command on your PATH.

## Usage

```bash
# Add a task
todo add "Finish DSA sheet" -p high -d 2026-06-25 -c study

# List pending tasks
todo list

# List everything, including completed tasks
todo list --all

# Filter by category, priority, or search text
todo list -c study
todo list -p high
todo list -s "DSA"

# Mark a task done
todo done 1

# Delete a task
todo delete 1
```

### Command reference

| Command | Description | Options |
|---|---|---|
| `add <title>` | Add a new task | `-p/--priority`, `-d/--due`, `-c/--category` |
| `list` | List tasks | `-a/--all`, `-c/--category`, `-p/--priority`, `-s/--search` |
| `done <id>` | Mark a task complete | — |
| `delete <id>` | Delete a task | — |

Tasks are stored in a local SQLite database at `~/.todo_cli/todo.db`.

## Project structure

```
todo-cli/
├── todo_cli/
│   ├── __init__.py
│   ├── __main__.py      # python -m todo_cli entry point
│   ├── cli.py            # argparse commands & output formatting
│   ├── database.py       # SQLite persistence layer
│   └── models.py         # Task dataclass + validation
├── tests/
│   └── test_database.py
├── pyproject.toml
└── README.md
```

## Running tests

```bash
pip install pytest
pytest tests/ -v
```

## Design notes

- **SQLite over flat files**: chosen to demonstrate proper persistence layer design (parameterized queries, schema migrations-ready structure) rather than ad-hoc JSON parsing.
- **Dataclass validation**: `Task` validates priority and due date format at construction time, catching bad data early.
- **Separation of concerns**: CLI parsing (`cli.py`) is decoupled from persistence (`database.py`) and the data model (`models.py`), making each independently testable.

## Possible extensions

- Recurring tasks
- Export to CSV/JSON
- `edit` command for updating existing tasks
- Color-coded terminal output via `rich`

## License

MIT
