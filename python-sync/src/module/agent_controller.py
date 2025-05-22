from fastapi import APIRouter, status, Form, File, UploadFile, Header
from fastapi.exceptions import ResponseValidationError
from pydantic import ValidationError
from typing import List, Optional

from src.common.helpers import handle_controller_error, create_status
from src.common.common_models import ErrorOutputDTO

from src.module.agent_models import Task
from src.module.agent_service import process_message_service, list_tasks_service, read_task_service, update_task_service, create_task_service, remove_task_service

router = APIRouter(tags=["agent"])

@router.post("/messages")
async def message_controller(
    id_team_agent: str = Form(...),
    id_team: str = Form(...),
    id_task: str = Form(...),
    text: str = Form(...),  
    images: List[UploadFile] = File([]),
    videos: List[UploadFile] = File([]),
    audios: List[UploadFile] = File([]),
    documents: List[UploadFile] = File([])
):
    try:
        logger.info(f"message_controller: {text}, images: {len(images)}, videos: {len(videos)}, audios: {len(audios)}, documents: {len(documents)}")

        service_response = await process_message_service(
            id_team_agent=id_team_agent,
            id_team=id_team,
            id_task=id_task,
            text=text,
            images=images,
            videos=videos,
            audios=audios,
            documents=documents
        )

        return service_response

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/{id_team_agent}", response_model=List[Task])
async def list_tasks(id_team_agent: str):
    return await list_tasks_service(id_team_agent)

@router.get("/tasks/{id_team_agent}/{id_task}")
async def read_task(id_team_agent: str, id_task: str):
    task = await read_task_service(id_team_agent, id_task)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{id_team_agent}/{id_task}", response_model=Task)
async def update_task(
    id_team_agent: str,
    id_task: str,
    driver: str = Form(...)
):
    return await update_task_service(id_team_agent, id_task, driver)

@router.post("/tasks/{id_team_agent}", response_model=Task)
async def create_task(
    id_team_agent: str,
    id_team: str = Form(...),
    text: str = Form(...)
):

    new_task = await create_task_service(id_team_agent, id_team, text)
    return await read_task_service(id_team_agent, new_task.id_task)

@router.delete("/tasks/{id_team_agent}/{id_task}")
async def remove_task(id_team_agent: str, id_task: str):
    result = await remove_task_service(id_team_agent, id_task)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success", "message": "Task deleted"}