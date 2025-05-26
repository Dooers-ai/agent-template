from fastapi import APIRouter, status, HTTPException, Request
from typing import List
import logging

from src.module.task_services import (
    list_tasks_service,
    read_task_service,
    create_task_service,
    remove_task_service,
)

from src.module.task_models import Task

logger = logging.getLogger("dooers-agent-template")

router = APIRouter(tags=["task"])


@router.get(
    "/tasks/{id_team_agent}",
    response_model=List[Task],
    summary="List Tasks",
    status_code=status.HTTP_200_OK,
)
async def list_tasks(id_team_agent: str):
    try:
        logger.info(f"list_tasks: {id_team_agent}")
        return await list_tasks_service(id_team_agent)
    except Exception as e:
        logger.error(f"list_tasks error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/tasks/{id_team_agent}/{id_task}",
    response_model=Task,
    summary="Read Task",
    status_code=status.HTTP_200_OK,
)
async def read_task(id_team_agent: str, id_task: str):
    try:
        logger.info(f"read_task: {id_team_agent}, {id_task}")
        task = await read_task_service(id_task)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception as e:
        logger.error(f"read_task error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/tasks/{id_team_agent}",
    response_model=Task,
    summary="Create Task",
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    id_team_agent: str, request: Request
):
    try:
        input_form_data = await request.form()
        logger.info(f"create_task: {id_team_agent}")
        new_task = await create_task_service(id_team_agent, input_form_data)
        return await read_task_service(new_task.id_task)
    except Exception as e:
        logger.error(f"create_task error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/tasks/{id_team_agent}/{id_task}",
    summary="Remove Task",
    status_code=status.HTTP_200_OK,
)
async def remove_task(id_team_agent: str, id_task: str):
    try:
        logger.info(f"remove_task: {id_team_agent}, {id_task}")
        result = await remove_task_service(id_task)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "success", "message": "task deleted"}
    except Exception as e:
        logger.error(f"remove_task error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
