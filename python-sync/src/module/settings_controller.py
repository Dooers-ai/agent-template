from fastapi import APIRouter, status, HTTPException, Request
import logging


from src.module.settings_services import (
    read_settings_service,
    sync_settings_service,
)

logger = logging.getLogger("dooers-agent-template")

router = APIRouter(tags=["settings"])


@router.get(
    "/settings/{id_team_agent}",
    response_model=dict,
    summary="Read Settings",
    status_code=status.HTTP_200_OK,
)
async def read_settings(id_team_agent: str):
    try:
        service_result = await read_settings_service(id_team_agent)
        return service_result

    except Exception as e:
        logger.error(f"read_settings error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/settings/{id_team_agent}",
    response_model=dict,
    summary="Sync Settings",
    status_code=status.HTTP_200_OK,
)
async def sync_settings(id_team_agent: str, request: Request):
    try:
        input_form_data = await request.form()
        service_result = await sync_settings_service(id_team_agent, input_form_data)
        return service_result

    except Exception as e:
        logger.error(f"sync_settings error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
