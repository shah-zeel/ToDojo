import unittest
import os
import json
from datetime import datetime
from todojo.cmd.todo_manager import (
    add_todo,
    update_todo,
    delete_todo,
    _load_todos,
    _save_todos,
)
from todojo.models.tasks import Todo, Status
import contextlib


class TestTodoManager(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test_todos.json file for testing."""
        self.test_file = "test_todos.json"
        self.test_todo = {
            "id": 1,
            "description": "Test todo",
            "status": Status.TODO,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
        }
        _save_todos([self.test_todo], self.test_file)  # Initialize with one todo

    def tearDown(self):
        """Remove the test test_todos.json file after tests."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)  # Uncommented to ensure cleanup

    @contextlib.contextmanager
    def suppress_output(self):
        """Context manager to suppress stdout."""
        with open(os.devnull, "w") as devnull:
            with contextlib.redirect_stdout(devnull):
                yield

    def display_test_result(self, test_name, success):
        """Display the result of a test in a formatted block."""
        status = "SUCCESS" if success else "FAILURE"
        print(f"\nTest: {test_name}\nStatus: {status}\n{'=' * 30}")

    def test_add_todo(self):
        """Test adding a new todo."""
        test_name = "Test adding a new todo"
        with self.suppress_output():
            add_todo("New test todo", self.test_file)
        todos = _load_todos(self.test_file)
        success = len(todos) == 2 and todos[-1]["description"] == "New test todo"
        self.display_test_result(test_name, success)

    def test_update_todo(self):
        """Test updating an existing todo."""
        test_name = "Test updating an existing todo"
        with self.suppress_output():
            update_todo(1, "done", self.test_file)
        todos = _load_todos(self.test_file)
        success = todos[0]["status"] == Status.DONE.value
        self.display_test_result(test_name, success)

    def test_delete_todo(self):
        """Test deleting an existing todo."""
        test_name = "Test deleting an existing todo"
        with self.suppress_output():
            delete_todo(1, self.test_file)
        todos = _load_todos(self.test_file)
        success = len(todos) == 0
        self.display_test_result(test_name, success)

    def test_load_todos_empty_file(self):
        """Test loading todos from an empty file."""
        test_name = "Test loading todos from an empty file"
        _save_todos([], self.test_file)  # Save an empty list
        todos = _load_todos(self.test_file)
        success = todos == []
        self.display_test_result(test_name, success)

    def test_load_todos_invalid_json(self):
        """Test loading todos from a file with invalid JSON."""
        test_name = "Test loading todos from a file with invalid JSON"
        with open(self.test_file, "w") as f:
            f.write("invalid json")
        with self.suppress_output():
            todos = _load_todos(self.test_file)
        success = todos == []
        self.display_test_result(test_name, success)


if __name__ == "__main__":
    unittest.main()
