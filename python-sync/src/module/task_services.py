from typing import List, Dict
import time
import logging
import uuid

from src.module.ai_services import generate_title

from src.module.task_models import Task, Thread
from src.module.message_models import MessageRequest

logger = logging.getLogger("dooers-agent-template")

tasks_table: Dict[str, Task] = {}


async def list_tasks_service(id_team_agent: str) -> List[Task]:
    tasks = [
        task for task in tasks_table.values() if task.id_team_agent == id_team_agent
    ]
    logger.info(f"tasks listed: {id_team_agent}")
    return tasks


async def read_task_service(id_task: str) -> Task:
    task = tasks_table.get(id_task)
    logger.info(f"task read: {id_task}")
    return task


async def update_task_service(id_task: str, task: Task) -> Task:
    if task:
        task.updated_at = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        tasks_table[id_task] = task
    logger.info(f"task updated: {id_task}")
    return task


async def create_task_service(id_team_agent: str, form_data: dict) -> Task:
    id_task = str(uuid.uuid4())
    title = await generate_title(form_data["text"])
    created_at = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

    new_task = Task(
        id_task=id_task,
        id_team_agent=id_team_agent,
        id_team=form_data["id_team"],
        title=title,
        content=[],
        driver="auto",
        created_at=created_at,
        updated_at=created_at,
    )

    message_request = MessageRequest(
        id_team_agent=id_team_agent, id_team=form_data["id_team"], id_task=id_task, text=form_data["text"]
    )

    thread = Thread(request=message_request, response=None)

    new_task.content = [thread]

    tasks_table[id_task] = new_task
    logger.info(f"task created: {id_task}")
    return new_task


async def remove_task_service(id_task: str) -> bool:
    task = await read_task_service(id_task)
    if task:
        del tasks_table[id_task]
        logger.info(f"task removed: {id_task}")
        return True
    return False
