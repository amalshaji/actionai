from datetime import datetime

import actionai

todos = []  # type: ignore


def add_todo(task: str):
    """Function to add a new todo"""
    todos.append(
        {
            "id": len(todos) + 1,
            "task": task,
            "completed": False,
            "created_at": datetime.now(),
            "completed_at": None,
        }
    )


def list_todos():
    """Function to list all todos"""
    return todos


def mark_todo_as_done(id: int):
    """Mark a todo as completed"""
    for todo in todos:
        if todo["id"] == id:
            todo["completed"] = True
            todo["completed_at"] = datetime.now()


action = actionai.ActionAI()


action.register(add_todo)
action.register(list_todos)
action.register(mark_todo_as_done)

while True:
    x = input("Your query: ")
    print(action.prompt(x)["choices"][0]["message"]["content"])
    print("\n")


# Inputs
# q1: Add todo to water plants
# Get all todos
# I have watered the plants, can you mark the todo as done?
# List all todos, with date.
