import pytest
from unittest.mock import MagicMock, patch
from app.services.markets import MarketService

from config import SAMPLE_MARKETS_DATA, SAMPLE_MARKET_DATA_ID_1


@pytest.fixture
def market_service():
    return MarketService()


class TestMarketService:
    @patch.object(MarketService, "_get", return_value=SAMPLE_MARKETS_DATA)
    def test_market_service_get_all(self, mock_get, market_service):
        # Call the get_all method
        response = market_service.get_all()

        # Assert that requests.get was called with the expected path
        mock_get.assert_called_once_with("markets")

        # Assert that the response data matches the expected data
        assert response == SAMPLE_MARKETS_DATA

    @patch.object(MarketService, "_get", return_value=SAMPLE_MARKET_DATA_ID_1)
    def test_market_service_get_one_by_id(self, mock_get, market_service):
        # Define a sample market ID
        market_id = "market_1"

        # Call the get_one_by_id method
        response = market_service.get_one_by_id(market_id)

        # Assert that requests.get was called with the expected path
        mock_get.assert_called_once_with(f"markets/{market_id}")

        # Assert that the response data matches the expected data
        assert response == SAMPLE_MARKET_DATA_ID_1
