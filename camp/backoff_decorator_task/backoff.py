import itertools
import time
import typing
from functools import wraps

from camp.backoff_decorator_task.backoff_exceptions import MaxTriesException

ReturnT = typing.TypeVar("ReturnT")
ParamsT = typing.ParamSpec("ParamsT")
DEFAULT_DELAY = 0


def backoff(
    exceptions: tuple[type[BaseException], ...] | type[BaseException],
    max_retry_attempts: int | None = 3,
    delay: int = DEFAULT_DELAY,
) -> typing.Callable[
    [typing.Callable[ParamsT, ReturnT]],
    typing.Callable[ParamsT, ReturnT],
]:
    """Call a function if exception raise.

    Args:
        exceptions: Rising exceptions.
        max_retry_attempts: number of attempts.
            if number is None, the function is called infinitely.
        delay: delay between attempts.

    Raises:
        MaxTriesException: if max_retry_attempts was reached.

    """
    if max_retry_attempts is not None and max_retry_attempts < 0:
        raise ValueError("'max_retry_attempts' must be non-negative or None.")

    def decorator_builder(
        func: typing.Callable[ParamsT, ReturnT],
    ) -> typing.Callable[ParamsT, ReturnT]:
        @wraps(func)
        def wrapper(
            *args: ParamsT.args,
            **kwargs: ParamsT.kwargs,
        ) -> ReturnT:
            attempts = itertools.cycle(
                [None],
            ) if max_retry_attempts is None else range(max_retry_attempts + 1)
            for _ in attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    time.sleep(delay / 1000)

            raise MaxTriesException(
                f"Function '{func.__name__}' failed, "
                f"reached {max_retry_attempts} attempts.",
            )
        return wrapper
    return decorator_builder
