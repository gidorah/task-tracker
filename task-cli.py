import json
from datetime import datetime
import argparse
import textwrap

# Task states
TODO = "todo"
IN_PROGRESS = "in-progress"
DONE = "done"
DELETED = "deleted"


# Commands
ADD = "add"
UPDATE = "update"
DELETE = "delete"
MARK_IN_PROGRESS = "mark-in-progress"
MARK_DONE = "mark-done"
LIST = "list"

JSON_FILE = "tasks.json"

task_list = []

arg_parser = argparse.ArgumentParser(
    prog="task-cli",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=(
        """
example usages:

    # Adding a new task
    task-cli add "Buy groceries"

    # Updating and deleting tasks
    task-cli update 1 "Buy groceries and cook dinner"
    task-cli delete 1

    # Marking a task as in progress or done
    task-cli mark-in-progress 1
    task-cli mark-done 1

    # Listing all tasks
    task-cli list

    # Listing tasks by status
    task-cli list done
    task-cli list todo
    task-cli list in-progress
    """
    ),
)

arg_parser.add_argument(
    "command",
    help="First argument. It is the command that would have options. [add, update, delete, mark-in-progress, mark-done, list]",
)
arg_parser.add_argument("first_option", nargs="?")
arg_parser.add_argument("second_option", nargs="?")
args = arg_parser.parse_args()


def _get_new_id() -> int:
    """Create a unique ID for task"""

    if not task_list:
        return 0

    return len(task_list)


class Task:
    id: int
    description: str
    status: str
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        id: int = None,
        description: str = None,
        status: str = TODO,
        created_at: str = None,
        updated_at: str = None,
    ):
        if id is None:
            id = _get_new_id()
        self.id = id

        self.description = description
        self.status = status

        if created_at is None:
            created_at = datetime.now().isoformat()
        self.created_at = datetime.fromisoformat(created_at)

        if updated_at is None:
            updated_at = created_at
        self.updated_at = datetime.fromisoformat(updated_at)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


def save_to_json(func):
    """Decorator to save current state of task_list to file after function call"""

    def wrapper(*args, **kwargs):
        # Call the original function and store its result
        result = func(*args, **kwargs)

        # Convert task_list to JSON and print it
        json_str = json.dumps([task.to_dict() for task in task_list], indent=4)
        with open(JSON_FILE, mode="w", encoding="utf-8") as json_file:
            json_file.write(json_str)
            json_file.close()

        # Return the original function's result
        return result

    return wrapper


def load_json():
    """Loads data from json file to task_list"""
    with open(JSON_FILE, mode="r", encoding="utf-8") as json_file:
        json_str = json_file.read()
        json_file.close()

        if not json_str:
            return

        data = json.loads(json_str)

        loaded_tasks = [Task(**item) for item in data]

        task_list.clear()
        task_list.extend(loaded_tasks)


@save_to_json
def add_task(description: str):
    """Create a new task"""
    new_task = Task(description=description)
    task_list.append(new_task)
    print(f"Task added successfully (ID:{new_task.id})")


@save_to_json
def update_task(id: int, new_description: str):
    """Update task description by id"""
    task = task_list[id]
    task.description = new_description
    task.updated_at = datetime.now()


@save_to_json
def change_task_status(id: int, new_status: str):
    """Change task status by id"""
    task = task_list[id]
    task.status = new_status
    task.updated_at = datetime.now()


@save_to_json
def delete_task(id: int):
    """Mark task as deleted"""
    task = task_list[id]
    task.status = DELETED
    task.updated_at = datetime.now()


def list_tasks(filter_status: str = None):
    """List undeleted tasks, filter if status given"""
    for task in task_list:
        if (
            filter_status is not None
            and task.status == filter_status
            or filter_status is None
            and task.status != DELETED
        ):
            print(f"{task.id}: {task.description}")


if __name__ == "__main__":
    load_json()

    try:
        if args.command == ADD:
            add_task(args.first_option)
        elif args.command == UPDATE:
            task_id = int(args.first_option)
            update_task(task_id, args.second_option)
        elif args.command == MARK_IN_PROGRESS:
            task_id = int(args.first_option)
            change_task_status(id=task_id, new_status=IN_PROGRESS)
        elif args.command == MARK_DONE:
            task_id = int(args.first_option)
            change_task_status(id=task_id, new_status=DONE)
        elif args.command == DELETE:
            task_id = int(args.first_option)
            delete_task(id=task_id)
        elif args.command == LIST:
            list_tasks(filter_status=args.first_option if args.first_option else None)
    except IndexError:
        print(f"There is no task with id: {task_id}")
    except:
        print("Wrong Usage!\n")
        arg_parser.print_help()
