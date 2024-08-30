from typing import Any

import pytest
from pytest_mock import MockerFixture

from camp.github_task.main import GitHubRepository


@pytest.fixture(scope="session")
def github_repo() -> GitHubRepository:
    """Create an instance of GitHubRepository."""
    return GitHubRepository(
        owner="test_owner",
        repo="test_repo",
        token="test_token",
    )


def mock_api_response(
    mocker: MockerFixture,
    response_data_list: list[list[dict[str, Any]]],
    links_list: list[dict[str, Any]] | None = None,
) -> None:
    """Mock the responses of the GitHub API."""
    fake_responses = []
    for i, response_data in enumerate(response_data_list):
        fake_response = mocker.MagicMock()
        fake_response.json.return_value = response_data
        fake_response.links = (
            links_list[i] if links_list and i < len(links_list) else {}
        )
        fake_responses.append(fake_response)
    mocker.patch("requests.get", side_effect=fake_responses)


@pytest.mark.parametrize(
    "response_data_list",
    [
        [
            {
                "login": "user1",
                "contributions": 10,
            },
            {
                "login": "user2",
                "contributions": 5,
            },
        ],

    ],
)
def test_get_json_response(
    github_repo: GitHubRepository,
    mocker: MockerFixture,
    response_data_list: list[dict[str, Any]],
) -> None:
    """Test the get_json_response method of GitHubRepository.

    Mock the requests.get method to simulate an API response.

    """
    mock_api_response(
        mocker,
        response_data_list=[response_data_list],
        links_list=[
            {
                "next": {"next": "https://commits?page=2"},
            },
        ],
    )
    url = "https://api.github.com/repos/contributors"
    params = {"page": 1, "per_page": 100}
    response = github_repo.get_json_response(url, params)
    assert response == response_data_list


@pytest.mark.parametrize(
    "response_data_list",
    [
        [
            {"login": "user1"},
            {"login": "user2"},
            {"login": "user3"},
            {"login": "user1"},
        ],

    ],
)
def test_get_unique_users(
    github_repo: GitHubRepository,
    mocker: MockerFixture,
    response_data_list: list[dict[str, Any]],
) -> None:
    """Test method get_unique_users of class GitHubRepository.

    Mock object from GitHub API and return a list of users with duplicates
    and checks that method returned unique usernames

    """
    mock_api_response(
        mocker,
        response_data_list=[response_data_list],
        links_list=[{
            "next": {"next": "https://commits?page=2"},
        }],
    )

    users = github_repo.get_unique_users()
    expected_users = {"user1", "user2", "user3"}
    actual_users = {user["login"] for user in response_data_list}
    assert len(users) == len(actual_users)
    assert expected_users == actual_users


@pytest.mark.parametrize(
    ["response_data_list", "expected_commits_count"],
    [
        [
            [
                {
                    "commit": "commit1",
                    "author": {"login": "user1"},
                },
                {
                    "commit": "commit2",
                    "author": {"login": "user2"},
                },
                {
                    "commit": "commit3",
                    "author": {"login": "user3"},
                },
                {
                    "commit": "commit4",
                    "author": {"login": "user2"},
                },
            ],
            4,
        ],
    ],
)
def test_get_commits_last_month(
    github_repo: GitHubRepository,
    mocker: MockerFixture,
    response_data_list: list[list[dict[str, Any]]],
    expected_commits_count: int,
) -> None:
    """Test method get_commits_last_month of class GitHubRepository.

    Mock object from GitHub API and returns a list of users and checks
    that method returned correct number

    """
    mock_api_response(
        mocker,
        response_data_list=response_data_list,
        links_list=[
            {"next": {"url": "https://commits?page=2"}},
            {"prev": {"url": "https://commits?page=1"}},
        ],
    )
    commits = github_repo.get_commits_last_month()

    assert commits == expected_commits_count


@pytest.mark.parametrize(
    ["response_data_list", "expected_committer", "expected_contributions"],
    [
        [
            [
                {"login": "user1", "contributions": 5},
                {"login": "user2", "contributions": 10},
                {"login": "user3", "contributions": 3},
            ],
            "user2",
            10,
        ],
        [
            [
                {"login": "user4", "contributions": 8},
                {"login": "user5", "contributions": 8},
                {"login": "user6", "contributions": 6},
            ],
            "user4",
            8,
        ],
    ],
)
def test_get_the_most_active_committer(
    github_repo: GitHubRepository,
    mocker: MockerFixture,
    response_data_list: list[dict[str, Any]],
    expected_committer: str,
    expected_contributions: int,
) -> None:
    """Test method get_the_most_active_committer of class GitHubRepository.

    Mock object from GitHub API and return a list of users with their
    contributions and checks that method returned correct most active user and
    number of contributions

    """
    mock_api_response(
        mocker,
        [response_data_list],
        links_list=[{
            "prev": {"url": "https://commits?page=1"},
        }],
    )

    committer, contributions = github_repo.get_the_most_active_committer()

    assert committer == expected_committer
    assert contributions == expected_contributions
