from typing import Optional

from src.common.abstracts.base_exception import BaseException
from src.common.constants import DescriptionCodes, StatusCodes


class InterfaceException(BaseException):
    def __init__(
        self,
        description: DescriptionCodes,
        code: StatusCodes,
        message: Optional[str] = None,
        detail: Optional[str] = None,
        error: Optional[Exception] = None,
    ):
        super().__init__(
            type="INTERFACE",
            name="Interface Exception",
            description=description,
            code=code,
            message=message,
            detail=detail,
            scope="INTERFACE",
            is_error=True,
            error=error,
        )
