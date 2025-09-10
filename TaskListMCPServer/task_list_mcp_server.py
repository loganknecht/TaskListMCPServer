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
        A json object encoded as a string of all tasks
    """
    task_list_data = listJsonFileContents()

    return json.dumps(task_list_data, indent=4)


@mcp.tool()
async def findTask(search_query: str) -> str:
    """Find a task using a query

    Args:
        search_query: the search query to match in all tasks

    Returns:
        A json object encoded as a string that is the tasks that matched the search query
    """
    pass

@mcp.tool()
def createTask(title: str, description: str):
    """Creates a new task

    Args:
        title: The title of the task
        description: The description of the task

    Returns:
        ?????
    """
    task_id = str(uuid.uuid4())

    new_task: Task = {
        "id": task_id,
        "title": title,
        "description": description,
        "is_completed": False
    }

    addTaskToJsonFile(new_task)

    return None

@mcp.tool()
def deleteAllTasks():
    """Delete all tasks

    Args:

    Returns:
        ?????
    """
    deleteAllTasksFromJsonFile()

    return None