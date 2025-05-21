from typing import Optional

from src.common.abstracts.base_exception import BaseException
from src.common.constants import DescriptionCodes, StatusCodes


class ServerException(BaseException):
    def __init__(
        self,
        description: DescriptionCodes,
        code: StatusCodes,
        message: Optional[str] = None,
        detail: Optional[str] = None,
        error: Optional[Exception] = None,
    ):
        super().__init__(
            type="SERVER",
            name="Server Exception",
            description=description,
            code=code,
            message=message,
            detail=detail,
            scope="SERVER",
            is_error=True,
            error=error,
        )
