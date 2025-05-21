from pydantic import BaseModel
from typing import TypeVar, Generic, Union, Optional

from src.common.constants import StatusCodes, DescriptionCodes


class Status(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    description: DescriptionCodes
    code: StatusCodes
    message: Optional[str] = None
    detail: Optional[str] = None
    scope: Optional[str] = None
    is_error: Optional[bool] = False
    error: Optional[str] = None


class StatusOutputDTO(BaseModel):
    type: str
    name: str
    description: DescriptionCodes
    code: StatusCodes
    message: Optional[str] = None
    detail: Optional[str] = None
    scope: Optional[str] = None
    is_error: bool


class ErrorOutputDTO(BaseModel):
    output: None
    status: StatusOutputDTO

    model_config = {
        "json_schema_extra": {
            "example": {
                "output": None,
                "status": {
                    "type": "CLIENT_ERROR",
                    "name": "NOT_FOUND",
                    "description": DescriptionCodes.NOT_FOUND,
                    "code": StatusCodes.NOT_FOUND,
                    "message": "resource not found",
                    "detail": "account ID=1234567890 not found",
                    "scope": "ReadAccountService",
                    "isError": True,
                },
            }
        }
    }


T = TypeVar("T")
E = TypeVar("E")


class Success(Generic[T]):
    def __init__(self, result: T):
        self._tag = "success"
        self.result = result
        self.is_success = True
        self.is_failure = False


class Failure(Generic[E]):
    def __init__(self, result: E):
        self._tag = "failure"
        self.result = result
        self.is_success = False
        self.is_failure = True


Result = Union[Success[T], Failure[E]]
