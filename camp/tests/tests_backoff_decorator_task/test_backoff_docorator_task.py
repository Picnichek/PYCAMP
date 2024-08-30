import pytest

from camp.backoff_decorator_task import backoff as decorator


def test_max_retries_exceeded() -> None:
    """Test backoff decorator with custom error."""
    try_number = 0

    @decorator.backoff(
        exceptions=ValueError,
        max_retry_attempts=3,
    )
    def fails_function() -> None:
        nonlocal try_number
        try_number += 1
        raise ValueError
    with pytest.raises(decorator.MaxTriesException):
        fails_function()
    assert try_number == 4


@pytest.mark.parametrize("max_retry_number", [3, None])
def test_retries_and_succeed(max_retry_number: int | None) -> None:
    """Test backoff decorator with success after errors."""
    try_number = 0

    @decorator.backoff(
        exceptions=ValueError,
        max_retry_attempts=max_retry_number,
    )
    def retries_and_succeed() -> str:
        nonlocal try_number
        try_number += 1
        if try_number < 4:
            raise ValueError
        return "finish"

    assert retries_and_succeed() == "finish"


def test_negative_retry() -> None:
    """Test backoff decorator with negative number."""
    def create_function_with_negative_number() -> None:
        @decorator.backoff(
            exceptions=ValueError,
            max_retry_attempts=-1,
        )
        def fails_function() -> str:
            return "finish"
        fails_function()
    with pytest.raises(
        ValueError,
        match="'max_retry_attempts' must be non-negative or None.",
    ):
        create_function_with_negative_number()
