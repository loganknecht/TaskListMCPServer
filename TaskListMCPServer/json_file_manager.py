# Python
import json
import os
from typing import Any, List, TypedDict

class Task(TypedDict):
    """Task"""
    id: str
    title: str
    description: str
    is_completed: bool

class TaskList(TypedDict):
    """Task List"""
    tasks: List[Task]

JSON_FILE_PATH = os.environ['TASK_LIST_JSON_FILE']

def createJsonFileIfDoesNotExist(json_file_path: str):
    if(os.path.exists(json_file_path) is False):
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            default_json_contents = '{ "tasks": [] }'

            json_file.write(default_json_contents)

def listJsonFileContents() -> TaskList:
    createJsonFileIfDoesNotExist(JSON_FILE_PATH)

    with open(JSON_FILE_PATH, 'r') as json_file:
        task_list_data = json.load(json_file)
        return task_list_data

def addTaskToJsonFile(new_task: Task):
    createJsonFileIfDoesNotExist(JSON_FILE_PATH)

    with open(JSON_FILE_PATH, 'r') as json_file:
        task_list_data = json.load(json_file)

    task_list_data["tasks"].append(new_task)

    with open(JSON_FILE_PATH, 'w') as json_file:
        json.dump(task_list_data, json_file, indent=4)

def deleteAllTasksFromJsonFile():
    os.remove(JSON_FILE_PATH)
    createJsonFileIfDoesNotExist(JSON_FILE_PATH)

def deleteTaskFromJsonFile(task_uuid: str):
    createJsonFileIfDoesNotExist(JSON_FILE_PATH)

    with open(JSON_FILE_PATH, 'r') as json_file:
        task_list_data = json.load(json_file)

    filtered_tasks = [task for task in task_list_data["tasks"] if task["id"] != task_uuid]
    task_list_data["tasks"] = filtered_tasks

    with open(JSON_FILE_PATH, 'w') as json_file:
        json.dump(task_list_data, json_file, indent=4)
