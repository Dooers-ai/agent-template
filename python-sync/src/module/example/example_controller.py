from fastapi import APIRouter, status
from fastapi.exceptions import ResponseValidationError
from pydantic import ValidationError

from src.common.helpers import handle_controller_error, create_status
from src.common.common_models import ErrorOutputDTO

from src.module.example.example_models import (
    ReadExampleRequestDTO,
    ReadExampleResponseDTO,
)
from src.module.example.example_service import read_example_service

router = APIRouter(tags=["example"])


@router.get(
    "/{id}",
    summary="Read Example Resource",
    responses={
        status.HTTP_200_OK: {"model": ReadExampleResponseDTO},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorOutputDTO},
        status.HTTP_404_NOT_FOUND: {"model": ErrorOutputDTO},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorOutputDTO},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorOutputDTO},
    },
    status_code=status.HTTP_200_OK,
)
async def read_example_controller(id: str):
    try:
        input = ReadExampleRequestDTO(id=id)

        service = await read_example_service(input)

        if service.is_failure:
            raise service.result

        output = ReadExampleResponseDTO(
            output=service.result.output, status=create_status(service.result.status)
        )

        return output
    except (ValidationError, ResponseValidationError, Exception) as error:
        return handle_controller_error(error, "read_example_controller")
