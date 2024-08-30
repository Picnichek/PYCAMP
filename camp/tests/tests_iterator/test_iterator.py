import pytest
import requests_mock

from camp.iterator import main


def test_success_request(
    fake_url: str,
    responses: dict[str, dict[str, object]],
    expected_result: list[dict[str, str]],
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test successful request."""
    for url, data in responses.items():
        requests_mock.get(url, json=data)
    results = []
    for item in main.ApiFetcher(fake_url):
        results.append(item)

    assert results == expected_result


def test_response_without_results(
    fake_url: str,
    requests_mock: requests_mock.Mocker,
) -> None:
    """Test response without results."""
    fetcher = main.ApiFetcher(fake_url)
    requests_mock.get(
        f"{fake_url}?limit=10",
        json={
            "next": None,
            "results": None,
        },
    )
    with pytest.raises(
        StopIteration,
        match="There are no data",
    ):
        next(fetcher)


def test_request_without_url() -> None:
    """Test failed request without url."""
    fetcher = main.ApiFetcher("")
    with pytest.raises(
        StopIteration,
        match="There is no next url",
    ):
        next(fetcher)
