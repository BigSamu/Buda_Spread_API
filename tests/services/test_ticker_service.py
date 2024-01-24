import pytest
from unittest.mock import MagicMock, patch
from app.services.tickers import TickerService


@pytest.fixture
def ticker_service():
    return TickerService()


class TestTickerService:
    @patch.object(
        TickerService, "_get", return_value={"market_id": "123", "ticker": "some_data"}
    )
    def test_ticker_service_get_one_by_market_id(self, mock_get, ticker_service):
        # Define a sample market ID
        market_id = "123"

        # Call the get_one_by_market_id method
        response = ticker_service.get_one_by_market_id(market_id)

        # Assert that requests.get was called with the expected path
        mock_get.assert_called_once_with(f"markets/{market_id}/ticker")

        # Assert that the response data matches the expected data
        assert response == {"market_id": market_id, "ticker": "some_data"}
