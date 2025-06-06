import time
import logging
import io
import uuid
from fastapi import UploadFile
from typing import List, AsyncGenerator, Dict
from google import genai
import json
import asyncio

from src.module.agent_models import (
    MessageRequest,
    MessageResponse,
    Task,
    Thread,
    MessageChunkStarted,
    MessageChunkText,
    MessageChunkFinished,
    MessageChunkError,
)
from src.settings import settings


model_client = genai.Client(api_key=settings.AI_GOOGLE_GEMINI_API_KEY)

logger = logging.getLogger("dooers-agent-template")

tasks_database: Dict[str, Task] = {}


async def generate_title(message_text: str) -> str:
    system_prompt = f"""
    Based on the following message, generate a concise and informative title (max 6 words) that captures its main topic or intent.
    The title should be in the same language as the message.
    
    Message: {message_text}
    
    Title:
    """

    response = model_client.models.generate_content(
        model=settings.AI_GOOGLE_GEMINI_MODEL, contents=system_prompt
    )

    title = response.text.strip()

    return title


async def prepare_content(
    text: str,
    images: List[UploadFile] = None,
    videos: List[UploadFile] = None,
    audios: List[UploadFile] = None,
    documents: List[UploadFile] = None,
) -> List:
    model_content = []

    system_prompt = "You are a helpful assistant. You are given a task to help the user with their request."

    model_content.append(system_prompt)
    model_content.append(text)

    uploaded_files = []

    if images and len(images) > 0:
        for image in images:
            try:
                content = await image.read()
                file = model_client.files.upload(
                    file=io.BytesIO(content), config=dict(mime_type=image.content_type)
                )
                uploaded_files.append(file)
            except Exception as e:
                logger.error(f"error uploading image file: {str(e)}")

    if videos and len(videos) > 0:
        for video in videos:
            try:
                content = await video.read()
                file = model_client.files.upload(
                    file=io.BytesIO(content), config=dict(mime_type=video.content_type)
                )
                uploaded_files.append(file)
            except Exception as e:
                logger.error(f"error uploading video file: {str(e)}")

    if audios and len(audios) > 0:
        for audio in audios:
            try:
                content = await audio.read()
                file = model_client.files.upload(
                    file=io.BytesIO(content), config=dict(mime_type=audio.content_type)
                )
                uploaded_files.append(file)
            except Exception as e:
                logger.error(f"error uploading audio file: {str(e)}")

    if documents and len(documents) > 0:
        for document in documents:
            try:
                content = await document.read()
                file = model_client.files.upload(
                    file=io.BytesIO(content),
                    config=dict(mime_type=document.content_type),
                )
                uploaded_files.append(file)
            except Exception as e:
                logger.error(f"error uploading document file: {str(e)}")

    if uploaded_files:
        model_content = uploaded_files + model_content

    return model_content


async def process_message_service(
    id_team_agent: str,
    id_team: str,
    id_task: str,
    text: str,
    images: List[UploadFile] = None,
    videos: List[UploadFile] = None,
    audios: List[UploadFile] = None,
    documents: List[UploadFile] = None,
) -> AsyncGenerator[str, None]:
    created_at = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

    model_content = await prepare_content(text, images, videos, audios, documents)

    try:
        response_stream = model_client.models.generate_content_stream(
            model=settings.AI_GOOGLE_GEMINI_MODEL, contents=model_content
        )

        started_chunk = MessageChunkStarted(
            event="started",
            id_team_agent=id_team_agent,
            id_team=id_team,
            id_task=id_task,
            created_at=created_at,
        )
        logger.info("[stream] sending started chunk")
        yield json.dumps(started_chunk.dict())

        response_text = ""
        chunk_count = 0

        for chunk in response_stream:
            chunk_text = chunk.text
            if chunk_text:
                response_text += chunk_text
                chunk_count += 1

                text_chunk = MessageChunkText(event="text-chunk", content=chunk_text)
                logger.debug(f"[stream] sending text chunk: {chunk_text}")
                yield json.dumps(text_chunk.dict())

                # avoid overwhelming the client
                if chunk_count % 5 == 0:
                    await asyncio.sleep(0.01)

        message_request = MessageRequest(
            id_team_agent=id_team_agent, id_team=id_team, id_task=id_task, text=text
        )

        message_response = MessageResponse(
            id_team_agent=id_team_agent,
            id_team=id_team,
            id_task=id_task,
            created_at=created_at,
            text=response_text,
            reasoning=None,
        )

        thread = Thread(request=message_request, response=message_response)

        task = await read_task_service(id_task)

        if task:
            task.content.append(thread)
            await update_task_service(id_task, task)

        finished_chunk = MessageChunkFinished(event="finished")
        logger.info("[stream] sending finished chunk")
        yield json.dumps(finished_chunk.dict())

    except Exception as e:
        logger.error(f"Error generating response stream: {str(e)}")

        error_message = (
            f"I'm sorry, I encountered an error while processing your request: {str(e)}"
        )

        error_chunk = MessageChunkError(event="error", error=error_message)
        logger.info(f"[stream] sending error chunk: {error_message}")
        yield json.dumps(error_chunk.dict())

        finished_chunk = MessageChunkFinished(event="finished")
        logger.info("[stream] sending finished chunk")
        yield json.dumps(finished_chunk.dict())

        raise


async def list_tasks_service(id_team_agent: str) -> List[Task]:
    tasks = [
        task for task in tasks_database.values() if task.id_team_agent == id_team_agent
    ]
    return tasks


async def read_task_service(id_task: str) -> Task:
    task = tasks_database.get(id_task)
    return task


async def update_task_service(id_task: str, task: Task) -> Task:
    if task:
        task.updated_at = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        tasks_database[id_task] = task
    return task


async def create_task_service(id_team_agent: str, id_team: str, text: str) -> Task:
    id_task = str(uuid.uuid4())
    title = await generate_title(text)
    created_at = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

    new_task = Task(
        id_task=id_task,
        id_team_agent=id_team_agent,
        id_team=id_team,
        title=title,
        content=[],
        driver="auto",
        created_at=created_at,
        updated_at=created_at,
    )

    message_request = MessageRequest(
        id_team_agent=id_team_agent, id_team=id_team, id_task=id_task, text=text
    )

    thread = Thread(request=message_request, response=None)

    new_task.content = [thread]

    tasks_database[id_task] = new_task

    return new_task


async def remove_task_service(id_task: str) -> bool:
    task = await read_task_service(id_task)
    if task:
        del tasks_database[id_task]
        return True
    return False
