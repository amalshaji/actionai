from datetime import datetime

import actionai

todos = {
    "jonas": [
        {
            "id": 1,
            "task": "drink milk",
            "completed": False,
            "created_at": "2023-07-08 21:39:46.828672",
            "completed_at": None,
        }
    ]
}  # type: ignore


def add_todo(task: str, user: str):
    """Function to add a new todo"""
    if user not in todos:
        todos[user] = []
    todos[user].append(
        {
            "id": len(todos) + 1,
            "task": task,
            "completed": False,
            "created_at": datetime.now(),
            "completed_at": None,
        }
    )


def list_todos(user: str):
    """Function to list all todos"""
    if user not in todos:
        todos[user] = []
    return todos[user]


def mark_todo_as_done(id: int, user: str):
    """Mark a todo as completed"""
    if user not in todos:
        todos[user] = []
    for todo in todos[user]:
        if todo["id"] == id:
            todo["completed"] = True
            todo["completed_at"] = datetime.now()


action = actionai.ActionAI(context={"user": "jason"})


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
