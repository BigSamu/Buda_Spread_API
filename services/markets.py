from services.base_api_client import BaseAPIClient
from typing import Dict, Any


class MarketService(BaseAPIClient):
    def get_all(self) -> Dict[str, Any]:
        """
        Retrieves all markets from the BUDA API.

        Returns:
            Dict[str, Any]: A dictionary containing the JSON response with all markets.
        """
        return self._get("markets")

