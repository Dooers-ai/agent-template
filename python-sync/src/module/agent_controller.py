from fastapi import APIRouter, status, Form, File, UploadFile, HTTPException
from typing import List
import logging

from src.module.agent_models import Task, MessageResponse
from src.module.agent_services import (
    process_message_service,
    list_tasks_service,
    read_task_service,
    update_task_service,
    create_task_service,
    remove_task_service,
)


logger = logging.getLogger("dooers-agent-template")

router = APIRouter(tags=["agent"])


@router.post(
    "/messages",
    response_model=MessageResponse,
    summary="Process Message",
    status_code=status.HTTP_200_OK,
)
async def run_message(
    id_team_agent: str = Form(...),
    id_team: str = Form(...),
    id_task: str = Form(...),
    text: str = Form(...),
    images: List[UploadFile] = File([]),
    videos: List[UploadFile] = File([]),
    audios: List[UploadFile] = File([]),
    documents: List[UploadFile] = File([]),
):
    try:
        logger.info(
            f"run_message [{id_team}/{id_team_agent}/{id_task}]:\nimages: {len(images)}, videos: {len(videos)}, audios: {len(audios)}, documents: {len(documents)}\ntext: {text}"
        )

        service_response = await process_message_service(
            id_team_agent=id_team_agent,
            id_team=id_team,
            id_task=id_task,
            text=text,
            images=images,
            videos=videos,
            audios=audios,
            documents=documents,
        )

        return service_response

    except Exception as e:
        logger.error(f"message_controller error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


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


@router.put(
    "/tasks/{id_team_agent}/{id_task}",
    response_model=Task,
    summary="Update Task",
    status_code=status.HTTP_200_OK,
)
async def update_task(
    id_team_agent: str,
    id_task: str,
):
    try:
        logger.info(f"update_task: {id_team_agent}, {id_task}")
        return await update_task_service(id_task)
    except Exception as e:
        logger.error(f"update_task error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/tasks/{id_team_agent}",
    response_model=Task,
    summary="Create Task",
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    id_team_agent: str, id_team: str = Form(...), text: str = Form(...)
):
    try:
        logger.info(f"create_task: {id_team_agent}, {id_team}, {text}")
        new_task = await create_task_service(id_team_agent, id_team, text)
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
