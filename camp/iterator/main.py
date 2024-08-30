import typing

import requests


class ApiFetcher:
    """Fetch data from api."""

    def __init__(self, url: str) -> None:
        self.url = url
        self.data = None

    def __next__(self) -> dict[str, typing.Any]:
        if self.data:
            return self.data.pop(0)
        if not self.url:
            raise StopIteration(
                "There is no next url",
            )
        response = requests.get(
            self.url,
            params={
                "limit": 10,
            },
            timeout=10,
        )
        response.raise_for_status()
        response_body = response.json()
        self.data = response_body.get("results")
        self.url = response_body.get("next")
        if not self.data:
            raise StopIteration("There are no data")
        return self.data.pop(0)

    def __iter__(self) -> typing.Self:
        return self
