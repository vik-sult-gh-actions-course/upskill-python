import os
from dotenv import load_dotenv
import requests
from typing import Dict, List, Optional
load_dotenv()

class SitesAPIClient:
    """
    A client for interacting with the SitesAPI.
    Handles authentication and provides methods to access API endpoints.
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the client with the API base URL.

        Args:
            base_url: The base URL of the SitesAPI (default: "http://localhost:8000")
        """
        self.base_url = base_url.rstrip('/')
        self.token = None

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
            Exception: If the request fails
        """
        url = f"{self.base_url}/user/signup"
        payload = {
            "fullname": fullname,
            "email": email,
            "password": password
        }
        params = {
            "password": os.getenv("SITES_API_PASSWORD")
        }

        try:
            response = requests.post(url, json=payload, params=params)
            response.raise_for_status()
            data = response.json()
            self.token = data.get("access_token")
            return self.token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Signup failed: {str(e)}")

    def get_list_of_sites(self, page: int = 0, limit: int = 10) -> Dict:
        """
        Retrieve a paginated list of sites.

        Args:
            page: Page number (0-based)
            limit: Number of items per page

        Returns:
            Dictionary containing sites data, total count, and current page

        Raises:
            Exception: If not authenticated or request fails
        """
        if not self.token:
            raise Exception("Not authenticated. Call signup() first.")

        url = f"{self.base_url}/get_list_of_sites"
        params = {
            "page": page,
            "limit": limit
        }
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch sites: {str(e)}")

    def get_all_sites(self, batch_size: int = 100) -> List[Dict]:
        """
        Retrieve all sites by making multiple requests (handles pagination automatically).

        Args:
            batch_size: Number of sites to fetch per request

        Returns:
            List of all sites

        Raises:
            Exception: If not authenticated or request fails
        """
        all_sites = []
        page = 0
        total = None

        while True:
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

        return all_sites


# Example usage
if __name__ == "__main__":
    # Initialize the client
    client = SitesAPIClient(base_url="http://localhost:8000")

    try:
        # Sign up a new user
        token = client.signup(
            fullname="John Doe",
            email="john.doe@example.com",
            password="securepassword123"
        )
        print(f"Successfully authenticated. Token: {token[:10]}...")

        # Get first page of sites (10 items)
        sites_page = client.get_list_of_sites(page=0, limit=10)
        print(f"First page contains {len(sites_page['data'])} sites out of {sites_page['total']}")

        # Get all sites (warning: might be a lot of data!)
        # all_sites = client.get_all_sites()
        # print(f"Fetched {len(all_sites)} sites in total")

    except Exception as e:
        print(f"Error: {str(e)}")