# task-tracker

A simple task tracker cli application. Uses JSON file (tasks.json) to save/load tasks. 

It is one of roadmap.sh backend projects: https://roadmap.sh/projects/task-tracker

# Usage:

## Adding a new task

    task-cli add "Buy groceries"


## Updating and deleting tasks

    task-cli update 1 "Buy groceries and cook dinner"
    task-cli delete 1


## Marking a task as in progress or done
    task-cli mark-in-progress 1
    task-cli mark-done 1


## Listing all tasks
    task-cli list

## Listing tasks by status

    task-cli list done
    task-cli list todo
    task-cli list in-progress