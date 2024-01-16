from base_api_client import BaseAPIClient
from typing import Dict, Any

class MarketService(BaseAPIClient):
    def get_all_markets(self) -> Dict[str, Any]:
        """
        Retrieves all markets from the BUDA API.

        Returns:
            Dict[str, Any]: A dictionary containing the JSON response with all markets.
        """
        return self._get("markets")

    def get_market_by_id(self, market_id: str) -> Dict[str, Any]:
        """
        Retrieves a specific market by its ID from the BUDA API.

        Args:
            market_id (str): The unique identifier for the market.

        Returns:
            Dict[str, Any]: A dictionary containing the JSON response for the specified market.
        """
        return self._get(f"markets/{market_id}")
