# Python
from typing import Any
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
    pass

@mcp.tool()
async def findTask(search_query: str) -> str:
    """Find a task using a query

    Args:
        search_query: the search query to match in all tasks

    Returns:
        A json object encoded as a string that is the tasks that matched the search query
    """
    pass
