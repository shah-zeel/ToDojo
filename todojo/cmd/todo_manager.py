import json
from datetime import datetime
from ..models.todo import Todo, Status
from rich.console import Console
from rich.table import Table
from rich import print


def _load_todos(file_path: str = "todos.json") -> list:
    """Load existing todos from the JSON file."""
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
            if not content:  # Check if the file is empty
                return []
            return json.loads(content)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"[red]Error: {file_path} is corrupted or contains invalid JSON.[/red]")
        return []


def _save_todos(todos: list, file_path: str = "todos.json") -> None:
    """Save the todos to the JSON file."""
    with open(file_path, "w") as f:
        json.dump(todos, f, default=str)


def add_todo(description: str, file_path: str = "todos.json") -> None:
    """Add a new todo item."""
    todos = _load_todos(file_path)
    new_id = (todos[-1]["id"] + 1) if todos else 1  # Handle empty todos list

    new_todo = Todo(
        id=new_id,
        description=description,
        status=Status.TODO.value,
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )

    todos.append(new_todo.__dict__)
    _save_todos(todos, file_path)
    print(f"[green]Added {description}[/green]")


def update_todo(todo_id: int, new_status: str, file_path: str = "todos.json") -> None:
    """Update the status of an existing todo item."""
    todos = _load_todos(file_path)
    for todo in todos:
        if todo["id"] == todo_id:
            todo["status"] = Status[new_status.upper()].value
            todo["updatedAt"] = datetime.now()
            _save_todos(todos, file_path)
            print(f"[green]Updated todo {todo_id} to status {new_status}.[/green]")
            return

    print(f"[red]Todo with id {todo_id} not found.[/red]")


def delete_todo(todo_id: int, file_path: str = "todos.json") -> None:
    """Delete a todo item by its ID."""
    todos = _load_todos(file_path)
    new_todos = [todo for todo in todos if todo["id"] != todo_id]  # Filter out the todo

    _save_todos(new_todos, file_path)
    if len(new_todos) < len(todos):  # Check if a todo was deleted
        print(f"[green]Deleted todo with id {todo_id}.[/green]")
    else:
        print(f"[red]Todo with id {todo_id} not found.[/red]")


def list_todos(status: str, file_path: str = "todos.json") -> None:
    """List all todos with the given status."""
    todos = _load_todos(file_path)
    if status:
        todos = [
            todo for todo in todos if todo["status"] == Status[status.upper()].value
        ]

    if not todos or len(todos) == 0:
        print(f"No todos with status [red]{status}[/red] found.")
        return

    table_title = f"Todos with status {status}" if status else "All Todos"

    table = Table(title=table_title, header_style="bold bright_green")
    columns = ["ID", "Description", "Status", "Created At", "Updated At"]
    for column in columns:
        table.add_column(column, style="white")

    for todo in todos:
        table.add_row(
            str(todo["id"]),
            todo["description"],
            Status(todo["status"]).name,
            todo["createdAt"],
            todo["updatedAt"],
        )
    console = Console()
    console.print(table)
