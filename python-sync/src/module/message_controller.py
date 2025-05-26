from fastapi import APIRouter, status, HTTPException, Request
import logging

from src.module.message_models import MessageResponse, MessageRequest
from src.module.message_services import process_message_service

logger = logging.getLogger("dooers-agent-template")

router = APIRouter(tags=["message"])


@router.post(
    "/messages",
    response_model=MessageResponse,
    summary="Process Message",
    status_code=status.HTTP_200_OK,
)
async def process_message(request: Request):
    try:

        input_form_data = await request.form()
        message_request = MessageRequest(**input_form_data)

        service_result = await process_message_service(message_request)

        return service_result

    except Exception as e:
        logger.error(f"process_message error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
