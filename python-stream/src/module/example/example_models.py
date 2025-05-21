from pydantic import BaseModel, field_validator

from src.common.common_models import Status, StatusOutputDTO
from src.common.constants import StatusCodes, DescriptionCodes


class ExampleEntity(BaseModel):
    id: str
    name: str
    age: int
    email: str


class ExampleEntityDTO(BaseModel):
    id: str
    name: str
    age: int
    email: str


class ReadExampleServiceInput(BaseModel):
    id: str


class ReadExampleServiceOutput(BaseModel):
    output: ExampleEntityDTO
    status: Status


class ReadExampleRequestDTO(BaseModel):
    id: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, v):
        if not v:
            raise ValueError("id is required")
        return v


class ReadExampleResponseDTO(BaseModel):
    output: ExampleEntityDTO
    status: StatusOutputDTO

    model_config = {
        "json_schema_extra": {
            "example": {
                "output": {
                    "id": "1",
                    "name": "Turing",
                    "age": 30,
                    "email": "turing@example.com",
                },
                "status": {
                    "type": "RESOURCE_READ",
                    "name": "READ_EXAMPLE",
                    "description": DescriptionCodes.RESOURCE_READ,
                    "code": StatusCodes.OK,
                    "message": "resource read",
                    "detail": "account ID=1234567890 not found",
                    "scope": "ReadAccountService",
                    "isError": False,
                },
            }
        }
    }
