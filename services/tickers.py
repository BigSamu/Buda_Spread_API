from services.base_api_client import BaseAPIClient
from typing import Dict, Any


class TickerService(BaseAPIClient):
    def get_all(self) -> Dict[str, Any]:
        """
        Retrieves all tickers from the BUDA API.

        Returns:
            Dict[str, Any]: A dictionary containing the JSON response with all tickers.
        """
        return self._get("markets/tickers")

    def get_one_by_market_id(self, market_id: str) -> Dict[str, Any]:
        """
        Retrieves the ticker for a specific market ID from the BUDA API.

        Args:
            market_id (str): The unique identifier for the market.

        Returns:
            Dict[str, Any]: A dictionary containing the JSON response for the specified market's ticker.
        """
        return self._get(f"markets/{market_id}/ticker")
