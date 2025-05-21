from src.common.exceptions import AppException
from src.common.helpers import failure, success
from src.common.common_models import Result, Status
from src.common.constants import StatusCodes, DescriptionCodes

from src.module.example.example_models import (
    ExampleEntity,
    ExampleEntityDTO,
    ReadExampleServiceInput,
    ReadExampleServiceOutput,
)

database = {
    "1": ExampleEntity(id="1", name="Turing", age=30, email="turing@example.com"),
    "2": ExampleEntity(id="2", name="Liskov", age=25, email="liskov@example.com"),
}


async def read_example_service(
    input: ReadExampleServiceInput,
) -> Result[ReadExampleServiceOutput, AppException]:
    if not input.id:
        return failure(
            AppException(
                description=DescriptionCodes.INVALID_INPUT,
                code=StatusCodes.BAD_REQUEST,
                message="input id is required",
                detail="ID field must be provided",
            )
        )

    resource = database.get(input.id)

    if not resource:
        return failure(
            AppException(
                description=DescriptionCodes.NOT_FOUND,
                code=StatusCodes.NOT_FOUND,
                message="resource not found",
                detail=f"Resource with id {input.id} not found",
            )
        )

    return success(
        ReadExampleServiceOutput(
            output=ExampleEntityDTO(
                id=resource.id,
                name=resource.name,
                age=resource.age,
                email=resource.email,
            ),
            status=Status(
                description=DescriptionCodes.RESOURCE_READ,
                code=StatusCodes.OK,
                message="resource read",
            ),
        )
    )
