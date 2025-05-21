import pytest

from src.module.example import read_example_service, ReadExampleServiceInput
from src.common.constants import StatusCodes, DescriptionCodes


@pytest.mark.asyncio
async def test_read_example_success():
    # arrange

    input = ReadExampleServiceInput(id="1")

    # act

    service = await read_example_service(input)

    # assert

    assert service.is_success
    assert service.result.status.code == StatusCodes.OK
    assert service.result.status.description == DescriptionCodes.RESOURCE_READ


@pytest.mark.asyncio
async def test_read_example_not_found_failure():
    # arrange

    input = ReadExampleServiceInput(id="999")

    # act

    service = await read_example_service(input)

    # assert

    assert service.is_failure
    assert service.result.status.code == StatusCodes.NOT_FOUND
    assert service.result.status.description == DescriptionCodes.NOT_FOUND
    assert service.result.status.is_error is True


@pytest.mark.asyncio
async def test_read_example_invalid_inpu_failure():
    # arrange

    input = ReadExampleServiceInput(id="")

    # act

    service = await read_example_service(input)

    # assert

    assert service.is_failure
    assert service.result.status.code == StatusCodes.BAD_REQUEST
    assert service.result.status.description == DescriptionCodes.INVALID_INPUT
    assert service.result.status.is_error is True
