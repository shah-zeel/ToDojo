import json
from datetime import datetime
from ..models.tasks import Todo, Status


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
        print(f"Error: {file_path} is corrupted or contains invalid JSON.")
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
    print(f"Added {description}")


def update_todo(todo_id: int, new_status: str, file_path: str = "todos.json") -> None:
    """Update the status of an existing todo item."""
    todos = _load_todos(file_path)
    for todo in todos:
        if todo["id"] == todo_id:
            todo["status"] = Status[new_status.upper()].value
            todo["updatedAt"] = datetime.now()
            _save_todos(todos, file_path)
            print(f"Updated todo {todo_id} to status {new_status}.")
            return

    print(f"Todo with id {todo_id} not found.")


def delete_todo(todo_id: int, file_path: str = "todos.json") -> None:
    """Delete a todo item by its ID."""
    todos = _load_todos(file_path)
    new_todos = [todo for todo in todos if todo["id"] != todo_id]  # Filter out the todo

    _save_todos(new_todos, file_path)
    if len(new_todos) < len(todos):  # Check if a todo was deleted
        print(f"Deleted todo with id {todo_id}.")
    else:
        print(f"Todo with id {todo_id} not found.")
