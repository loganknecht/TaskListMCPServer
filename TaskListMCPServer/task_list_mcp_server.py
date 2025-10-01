# Python
import json
import os
from typing import Any, TypedDict
import uuid
# Third-Party
from fastmcp import FastMCP
# Custom
from json_file_manager import *

mcp = FastMCP("TaskList")

@mcp.tool()
def listTasks() -> str:
    """List All Tasks

    Returns:
        A JSON object encoded as a string of all tasks
    """
    task_list_data = listJsonFileContents()

    return json.dumps(task_list_data, indent=4)


@mcp.tool()
async def findTask(search_query: str) -> str:
    """Find a task using a query

    Args:
        search_query: the search query to match in all tasks

    Returns:
        A JSON object encoded as a string that is the tasks that matched the search query
    """
    pass

@mcp.tool()
def createTask(title: str, description: str):
    """Creates a new task

    Args:
        title: The title of the task
        description: The description of the task

    Returns:
        A JSON object encoded as a string of the newly created task
    """
    task_id = str(uuid.uuid4())

    new_task: Task = {
        "id": task_id,
        "title": title,
        "description": description,
        "is_completed": False
    }

    addTaskToJsonFile(new_task)

    return json.dumps(new_task, indent=4)

@mcp.tool()
def deleteAllTasks():
    """Delete all tasks

    Args:

    Returns:
        None
    """
    deleteAllTasksFromJsonFile()

    return None

@mcp.tool()
def deleteTask(task_uuid: str):
    """Deletes a specific task

    Args:
        task_uuid - The id of the task to delete

    Returns:
        None
    """
    deleteTaskFromJsonFile(task_uuid)

    return None