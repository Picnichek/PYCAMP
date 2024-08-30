import typing

import pytest

pokemon_names = [
    "bulbasaur",
    "ivysaur",
    "venusaur",
    "charmander",
    "charmeleon",
    "charizard",
    "squirtle",
    "wartortle",
    "blastoise",
    "caterpie",
]


@pytest.fixture(scope="module")
def fake_url() -> str:
    """Url of fetched API."""
    return "https-mock://pokeapi.co/api/v2/pokemon"


@pytest.fixture
def expected_result(
    fake_url: str,
) -> list[dict[str, str]]:
    """Return expected data for tests."""
    return [
        {
            "name": name,
            "url": f"{fake_url}/{i + 1}/",
        } for i, name in enumerate(pokemon_names)
    ]


@pytest.fixture
def responses(
    fake_url: str,
) -> dict[str, dict[str, typing.Any]]:
    """Responses from api."""
    first_results = [
        {
            "name": name,
            "url": f"{fake_url}/{i + 1}/",
        } for i, name in enumerate(pokemon_names[:5])
    ]
    second_results = [
        {
            "name": name,
            "url": f"{fake_url}/{i + 6}/",
        } for i, name in enumerate(pokemon_names[5:])
    ]
    responses = {
        f"{fake_url}?limit=10": {
            "next": f"{fake_url}?offset=5&limit=5",
            "results": first_results,
        },
        f"{fake_url}?offset=5&limit=10": {
            "next": None,
            "results": second_results,
        },
    }
    return responses
