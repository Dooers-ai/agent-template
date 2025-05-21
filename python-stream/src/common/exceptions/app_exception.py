from typing import Optional

from src.common.abstracts.base_exception import BaseException
from src.common.constants import DescriptionCodes, StatusCodes


class AppException(BaseException):
    def __init__(
        self,
        description: DescriptionCodes,
        code: StatusCodes,
        message: Optional[str] = None,
        detail: Optional[str] = None,
        error: Optional[Exception] = None,
    ):
        super().__init__(
            type="APPLICATION",
            name="Application Exception",
            description=description,
            code=code,
            message=message,
            detail=detail,
            scope="APPLICATION",
            is_error=True,
            error=error,
        )
