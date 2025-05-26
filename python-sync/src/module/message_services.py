from fastapi import UploadFile
import time
import logging

from src.module.ai_services import process_content, prepare_content
from src.module.message_models import MessageRequest, MessageResponse
from src.module.task_models import Thread
from src.module.task_services import read_task_service, update_task_service

logger = logging.getLogger("dooers-agent-template")


async def process_message_service(message_request: MessageRequest) -> MessageResponse:

    # processing form data fields, including files
    for field_name, field_value in message_request.items():
        if isinstance(field_value, UploadFile):
            logger.info(
                f" settings_input: {field_name} → File: {field_value.filename or '(empty)'}"
            )
        else:
            logger.info(f" settings_input: {field_name} → {field_value}")

    # propare content for model requirements
    model_content = await prepare_content(
        message_request.text,
        message_request.images,
        message_request.videos,
        message_request.audios,
        message_request.documents,
    )

    created_at = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

    try:
        response_text = process_content(model_content)

        message_request = MessageRequest(
            id_team_agent=message_request.id_team_agent,
            id_team=message_request.id_team,
            id_task=message_request.id_task,
            text=message_request.text,
        )

        message_response = MessageResponse(
            id_team_agent=message_request.id_team_agent,
            id_team=message_request.id_team,
            id_task=message_request.id_task,
            created_at=created_at,
            text=response_text,
            reasoning=None,
        )

        thread = Thread(request=message_request, response=message_response)

        task = await read_task_service(message_request.id_task)

        if task:
            task.content.append(thread)
            await update_task_service(message_request.id_task, task)

        logger.info(f"message processed: {response_text[:150]}{'...' if len(response_text) > 150 else ''}")

        return message_response

    except Exception as e:
        logger.error(f"process_message_service error: {str(e)}")
        error_message = (
            f"I'm sorry, I encountered an error while processing your request: {str(e)}"
        )

        message_error_response = MessageResponse(
            id_team_agent=message_request.id_team_agent,
            id_team=message_request.id_team,
            id_task=message_request.id_task,
            created_at=created_at,
            text=error_message,
            is_error=True,
        )

        return message_error_response
