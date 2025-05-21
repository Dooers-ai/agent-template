import json
import traceback
from pydantic import ValidationError
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

from src.common.abstracts.base_exception import BaseException
from src.common.exceptions.interface_exception import InterfaceException
from src.common.exceptions.server_exception import ServerException
from src.common.helpers.status_helper import create_status
from src.common.common_models import Status, ErrorOutputDTO
from src.common.constants import StatusCodes, DescriptionCodes


def format_error(error):
    if isinstance(error, (ValidationError, ResponseValidationError)):
        try:
            if hasattr(error, "errors"):
                return json.dumps(error.errors(), indent=2)
            return str(error)
        except Exception:
            return str(error)
    elif isinstance(error, Exception):
        return f"{str(error)}\n{traceback.format_exc()}"
    return str(error)


def handle_controller_error(error: Exception, context: str) -> JSONResponse:
    if isinstance(error, BaseException):
        exception = error
        return JSONResponse(
            status_code=exception.status.code,
            content=ErrorOutputDTO(
                output=None,
                status=create_status(
                    Status(
                        description=exception.status.description,
                        code=exception.status.code,
                        message=exception.status.message,
                        detail=exception.status.detail,
                        scope=context,
                        is_error=exception.status.is_error,
                    )
                ),
            ).model_dump(),
        )

    if isinstance(error, (ValidationError, ResponseValidationError)):
        exception = InterfaceException(
            description=DescriptionCodes.VALIDATION_ERROR,
            code=StatusCodes.BAD_REQUEST,
            message="validation error",
            detail=format_error(error),
            error=format_error(error),
        )

        return JSONResponse(
            status_code=exception.status.code,
            content=ErrorOutputDTO(
                output=None,
                status=create_status(
                    Status(
                        description=exception.status.description,
                        code=exception.status.code,
                        message=exception.status.message,
                        detail=exception.status.detail,
                        scope=context,
                        is_error=exception.status.is_error,
                    )
                ),
            ).model_dump(),
        )

    exception = ServerException(
        description=DescriptionCodes.INTERNAL_SERVER_ERROR,
        code=StatusCodes.INTERNAL_SERVER_ERROR,
        message="an internal server error occurred",
        detail=format_error(error),
        error=format_error(error),
    )

    return JSONResponse(
        status_code=exception.status.code,
        content=ErrorOutputDTO(
            output=None,
            status=create_status(
                Status(
                    description=exception.status.description,
                    code=exception.status.code,
                    message=exception.status.message,
                    detail=exception.status.detail,
                    scope=context,
                    is_error=exception.status.is_error,
                )
            ),
        ).model_dump(),
    )
