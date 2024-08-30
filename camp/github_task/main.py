import argparse
import calendar
from collections import namedtuple
from datetime import datetime
from typing import Any
from urllib.parse import urlencode, urljoin

import requests

Contributor = namedtuple(
    "Contributor",
    ["login", "contributions"],
)
base_url = "https://api.github.com/repos"
JSON = list[dict[str, Any]]


class GitHubRepository:
    """Interact with the GitHub API for a specific repository."""

    def __init__(
        self,
        owner: str,
        repo: str,
        token: str,
    ) -> None:
        """Initialize a GitHubRepo instance with the owner, repository, token.

        Args:
            owner: The owner of the repository.
            repo: The name of the repository.
            token: The GitHub personal access token for authentication.

        """
        self.owner = owner
        self.repo = repo
        self.token = token
        self.base_url = f"{base_url}/{owner}/{repo}/"

    def get_json_response(
        self,
        url: str,
        params: dict[str, Any],
    ) -> JSON:
        """Return a json response of data from the GitHub API.

        Args:
            url: The API endpoint URL.
            params: The query parameters for the request.

        Returns:
            List of data from the response.

        """
        total_response: JSON = []
        headers = {
            "Authorization": f"Bearer {self.token}",
        } if self.token else {}
        full_url = f"{url}?{urlencode(params)}"
        response = requests.get(
            url=full_url,
            headers=headers,

        )
        response.raise_for_status()
        total_response.extend(response.json())

        next_url = response.links.get("next", {}).get("url")
        while next_url:
            response = requests.get(
                url=next_url,
                headers=headers,
            )
            response.raise_for_status()
            total_response.extend(response.json())
            next_url = response.links.get("next", {}).get("url")
        return total_response

    def get_unique_users(self) -> set[str]:
        """Fetch a list of unique users who made commit to the repository.

        Returns:
            Unique user logins.

        """
        url = urljoin(self.base_url, "contributors")
        unique_users: set[str] = set()
        params = {"page": 1, "per_page": 100}
        data = self.get_json_response(url, params)
        for user in data:
            unique_users.add(user["login"])
        return unique_users

    def get_commits_last_month(self) -> int:
        """Fetch a count of the commits in the last month.

        Returns:
            Number of commits in the last month.

        """
        year = datetime.now().year
        month = datetime.now().month - 1
        if month == 0:
            month = 12
            year -= 1
        days_in_month = calendar.monthrange(year, month)[1]
        since_date = str(
            (datetime(year, month, 1)).isoformat() + "Z",
        )
        until_date = str(
            (datetime(year, month, days_in_month)).isoformat() + "Z",
        )
        url = urljoin(self.base_url, "commits")
        count = 0
        params = {
            "page": 1,
            "per_page": 100,
            "since": since_date,
            "until": until_date,
        }
        data = self.get_json_response(url, params)
        count = len(data)

        return count

    def get_the_most_active_committer(self) -> Contributor:
        """Fetch the most active committer and their number of contributions.

        Returns:
            A named tuple with login and number of posts.

        """
        url = urljoin(self.base_url, "contributors")
        rating: JSON = []
        params = {
            "page": 1,
            "per_page": 100,
        }
        data = self.get_json_response(url, params)
        rating.extend(data)
        most_active_committer = max(
            rating,
            key=lambda x: x["contributions"],
        )

        return Contributor(
            most_active_committer["login"],
            most_active_committer["contributions"],
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="GitHub Repository Analysis",
    )
    parser.add_argument(
        "-o",
        "--owner",
        type=str,
        help="Owner of the Owner of the GitHub repository",
    )
    parser.add_argument(
        "-r",
        "--repo",
        type=str,
        help="Name of the GitHub repository",
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        help="GitHub personal access token",
    )
    args = parser.parse_args()

    repo = GitHubRepository(**vars(args))
    most_active = repo.get_the_most_active_committer()

    print(
        "Unique users:",
        repo.get_unique_users(),
    )
    print(
        "Commits for the last month:",
        repo.get_commits_last_month(),
    )
    print(
        "The most active committer:",
        most_active.login,
        most_active.contributions,
    )
