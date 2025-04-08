import argparse
import todojo.cmd.todo_manager as tm
from todojo.models.tasks import Status


def main():

    parser = argparse.ArgumentParser(
        prog="ToDoJo", description="A simple CLI app to track all your todos"
    )

    sub_parser = parser.add_subparsers(dest="command")

    add_parser = sub_parser.add_parser("add", help="Add a todo.")
    add_parser.add_argument("todo", type=str, help="Enter the description of the todo.")

    update_parser = sub_parser.add_parser("update", help="Update a todo.")
    update_parser.add_argument(
        "-id",
        "--id",
        required=True,
        type=int,
        help="Enter id of the todo you want to update.",
    )
    update_parser.add_argument(
        "-mark",
        "--mark-as",
        required=True,
        type=str,
        choices=[status.name.lower() for status in Status],  # Enum values as choices
        help="Updated status of the todo.",
    )

    delete_parser = sub_parser.add_parser("delete", help="Delete a todo.")
    delete_parser.add_argument(
        "-id",
        "--id",
        required=True,
        type=int,
        help="Enter id of the todo you want to delete.",
    )

    args = parser.parse_args()

    if args.command == "add":
        tm.add_todo(args.todo)
    elif args.command == "update":
        tm.update_todo(args.id, args.mark_as)
    elif args.command == "delete":
        tm.delete_todo(args.id)


if __name__ == "__main__":
    main()
