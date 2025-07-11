"""Client for interacting with the Sites API.

This module provides a client class for authenticating and making requests to the Sites API,
including user registration and site data retrieval functionality.
"""

import os
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException, HTTPError

load_dotenv()

DEFAULT_TIMEOUT = 30  # seconds


class SitesAPIClient:
    """
    A client for interacting with the sites_api.
    Handles authentication and provides methods to access API endpoints.
    """

    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        """
        Initialize the client with the API base URL.

        Args:
            base_url: The base URL of the sites_api (default: "http://localhost:8000")
        """
        self.base_url = base_url.rstrip("/")
        self.token: Optional[str] = None

    def signup(self, fullname: str, email: str, password: str) -> str:
        """
        Register a new user and obtain an access token.

        Args:
            fullname: User's full name
            email: User's email address
            password: User's password

        Returns:
            The access token

        Raises:
            HTTPError: If the HTTP request fails
            ValueError: If no access token is returned
            RuntimeError: If signup fails for other reasons
        """
        url = f"{self.base_url}/user/signup"
        payload = {"fullname": fullname, "email": email, "password": password}
        params = {"password": os.getenv("SITES_API_PASSWORD", "")}

        try:
            response = requests.post(
                url, json=payload, params=params, timeout=DEFAULT_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()

            # pylint: disable=redefined-outer-name
            if not (token := data.get("access_token")):
                raise ValueError("No access token in response")

            self.token = token
            return token

        except HTTPError as e:
            raise HTTPError(
                f"Signup failed with status {e.response.status_code}"
            ) from e
        except RequestException as e:
            raise RuntimeError(f"Signup request failed: {str(e)}") from e

    def get_list_of_sites(self, page: int = 0, limit: int = 10) -> Dict:
        """
        Retrieve a paginated list of sites.

        Args:
            page: Page number (0-based)
            limit: Number of items per page

        Returns:
            Dictionary containing sites data, total count, and current page

        Raises:
            RuntimeError: If not authenticated
            HTTPError: If the HTTP request fails
            RequestException: If the request fails for other reasons
        """
        if not self.token:
            raise RuntimeError("Not authenticated. Call signup() first.")

        url = f"{self.base_url}/get_list_of_sites"
        params = {"page": page, "limit": limit}
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        try:
            response = requests.get(
                url, params=params, headers=headers, timeout=DEFAULT_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            raise HTTPError(
                f"Failed to fetch sites with status {e.response.status_code}"
            ) from e
        except RequestException as e:
            raise RequestException(f"Failed to fetch sites: {str(e)}") from e

    def get_all_sites(self, batch_size: int = 100) -> List[Dict]:
        """
        Retrieve all sites by making multiple requests (handles pagination automatically).

        Args:
            batch_size: Number of sites to fetch per request

        Returns:
            List of all sites

        Raises:
            RuntimeError: If not authenticated or request fails
        """
        all_sites = []
        page = 0
        total = None

        while True:
            try:
                response = self.get_list_of_sites(page=page, limit=batch_size)

                # First iteration - get total count
                if total is None:
                    total = response.get("total", 0)

                # Add sites from current page
                all_sites.extend(response.get("data", []))

                # Check if we've fetched all sites
                if len(all_sites) >= total:
                    break

                page += 1
            except Exception as e:
                raise RuntimeError(f"Failed to retrieve all sites: {str(e)}") from e

        return all_sites


if __name__ == "__main__":
    # Initialize the client
    client = SitesAPIClient(base_url="http://localhost:8000")

    try:
        # Sign up a new user
        token = client.signup(
            fullname="John Doe",
            email="john.doe@example.com",
            password="securepassword123",
        )
        print(f"Successfully authenticated. Token: {token[:10]}...")

        # Get first page of sites (10 items)
        sites_page = client.get_list_of_sites(page=0, limit=10)
        print(
            f"First page contains {len(sites_page['data'])} sites out of {sites_page['total']}"
        )

    except HTTPError as e:
        print(f"HTTP Error occurred: {str(e)}")
    except RequestException as e:
        print(f"Request failed: {str(e)}")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Unexpected error: {str(e)}")
