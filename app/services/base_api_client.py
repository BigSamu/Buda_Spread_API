import requests
from config import settings
from typing import Any, Dict

from app.services.auth import BudaHMACAuth
from config import settings


class BaseAPIClient:
    def __init__(self) -> None:
        """
        Initializes the base API client with the base URL from settings.
        """
        self.base_url: str = settings.BUDA_API_URL

    def _get(self, path: str) -> Dict[str, Any]:
        """
        Makes a GET request to the specified path and returns the JSON response.

        Args:
            path (str): The API endpoint path to which the GET request is made.

        Returns:
            Dict[str, Any]: The parsed JSON response from the API.

        Raises:
            HTTPError: If the response contains an HTTP error status.
        """
        response = requests.get(
            f"{self.base_url}/{path}",
            auth=BudaHMACAuth(
                api_key=settings.BUDA_API_KEY, secret=settings.BUDA_API_SECRET
            ),
        )
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()
