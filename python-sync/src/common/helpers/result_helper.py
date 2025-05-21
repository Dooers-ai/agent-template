from src.common.common_models import Success, Failure, T, E


def success(output: T) -> Success[T]:
    return Success(output)


def failure(error: E) -> Failure[E]:
    return Failure(error)
