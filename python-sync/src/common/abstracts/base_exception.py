from typing import Optional
from src.settings import settings
from src.common.helpers.logger_helper import logger
from src.common.common_models import Status
from src.common.constants import StatusCodes, DescriptionCodes


class BaseException(Exception):
    def __init__(
        self,
        type: str,
        name: str,
        description: DescriptionCodes,
        code: StatusCodes,
        message: Optional[str] = None,
        detail: Optional[str] = None,
        scope: Optional[str] = None,
        is_error: bool = True,
        error: Optional[Exception] = None,
    ):
        self.status = Status(
            type=type,
            name=name,
            description=description,
            code=code,
            message=message,
            detail=detail,
            scope=scope,
            is_error=is_error,
            error=str(error) if error else None,
        )

        if error:
            logger.error(f"{self.status.name}: \n{error}")

        if settings.IS_DEVELOPMENT:
            logger.debug(
                f"{self.status.name}: \n{{\n"
                f"  description: {self.status.description}\n"
                f"  code: {self.status.code}\n"
                f"  message: {self.status.message}\n"
                f"  detail: {self.status.detail}\n"
                f"}}"
            )

        super().__init__(message or str(description))
