import pytest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from requests import Response, HTTPError

from app.main import app
from app.services.markets import MarketService
from app.services.tickers import TickerService

from config import settings

client = TestClient(app)


# Mock data for two different markets
mock_ticker_data_market_1 = {
    "ticker": {
        "market_id": "market_1",
        "max_bid": ["900", "CLP"],
        "min_ask": ["1000", "CLP"],
    }
}
mock_ticker_data_market_2 = {
    "ticker": {
        "market_id": "market_2",
        "max_bid": ["100", "CLP"],
        "min_ask": ["200", "CLP"],
    }
}
mock_markets_data = {"markets": [{"id": "market_1"}, {"id": "market_2"}]}


# Function to return different ticker data based on market ID
def _get_ticker_data_mock(market_id):
    if market_id == "market_1":
        return mock_ticker_data_market_1
    elif market_id == "market_2":
        return mock_ticker_data_market_2
    else:
        raise ValueError("Unknown market ID")

def _raise_http_error(detail: str, status_code: int):
    """Raise an HTTPError with the given detail and status code."""
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = status_code
    error = HTTPError(detail)
    error.response = mock_response
    return error


class TestGetAllSpreads:
    @patch.object(MarketService, "get_all", return_value=mock_markets_data)
    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_get_ticker_data_mock
    )
    def test_get_spreads_from_all_markets_succeeds(
        self,
        mock_get_one_ticker_by_market_id,
        mock_get_all_markets,
    ):
        number_of_markets = len(mock_markets_data["markets"])
        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/spreads")

        # Validate the response
        assert response.status_code == 200
        spreads = response.json()
        assert len(spreads) == number_of_markets

        # Check if MarketService.get_all was called once
        mock_get_all_markets.assert_called_once()
        assert mock_get_one_ticker_by_market_id.call_count == number_of_markets

        # Validate each market spread
        for spread in spreads:
            assert "market_id" in spread
            assert "max_bid" in spread
            assert "min_ask" in spread
            assert "value" in spread

    @patch.object(
        MarketService, "get_all", side_effect=_raise_http_error(detail="Internal Server Error", status_code=500)
    )
    def test_get_spreads_from_all_markets_fails_with_internal_server_error(
        self, mock_get_all_markets
    ):
        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/spreads")

        # Validate the response for internal server error
        assert response.status_code == 500
        error_response = response.json()
        assert "detail" in error_response
        assert (
            error_response["detail"]
            == "An unexpected error occurred: HTTPError: Internal Server Error"
        )

    @patch.object(MarketService, "get_all", return_value=mock_markets_data)
    @patch.object(
        TickerService,
        "get_one_by_market_id",
        side_effect=_raise_http_error(detail="Internal Server Error", status_code=500),
    )
    def test_get_all_spreads_internal_server_error_from_tickers(
        self, mock_get_one_ticker_by_market_id, mock_get_all_markets
    ):
        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/spreads")

        # Validate the response for internal server error
        assert response.status_code == 500
        error_response = response.json()
        assert "detail" in error_response
        assert (
            error_response["detail"]
            == "An unexpected error occurred: HTTPError: Internal Server Error"
        )


class TestGetSpreadByMarketId:
    # Test for successful data retrieval
    @patch.object(
        TickerService, "get_one_by_market_id", return_value=mock_ticker_data_market_1
    )
    def test_get_spread_by_market_id_succeeds(self, mock_get_one_by_market_id):
        market_id = "market_1"
        response = client.get(f"{settings.API_URL_PREFIX}/spreads/{market_id}")

        assert response.status_code == 200
        spread = response.json()
        assert spread["market_id"] == market_id
        assert spread["max_bid"] == "900.000000"
        assert spread["min_ask"] == "1,000.000000"
        # Add more assertions for other fields like spread_value

        # Verify the mock method was called correctly
        mock_get_one_by_market_id.assert_called_once_with(market_id=market_id)

    # Test for market not found (404 Error)
    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_raise_http_error(detail="Market not found", status_code=404)
    )
    def test_get_spread_by_market_id_fails_with_not_found_error(
        self, mock_get_one_by_market_id
    ):
        market_id = "unknown_market"
        response = client.get(f"{settings.API_URL_PREFIX}/spreads/{market_id}")

        assert response.status_code == 404
        assert f"Market with id '{market_id}' not found" in response.json().get(
            "detail", ""
        )

        # Verify the mock method was called correctly
        mock_get_one_by_market_id.assert_called_once_with(market_id=market_id)

    # Test for internal server error (500 Error)
    @patch.object(
        TickerService,
        "get_one_by_market_id",
        side_effect=_raise_http_error(detail="Internal Server Error", status_code=500),
    )
    def test_get_spread_by_market_id_internal_server_error(
        self, mock_get_one_by_market_id
    ):
        market_id = "market_1"
        response = client.get(f"{settings.API_URL_PREFIX}/spreads/{market_id}")

        assert response.status_code == 500
        assert "Internal Server Error" in response.json().get("detail", "")

        # Verify the mock method was called correctly
        mock_get_one_by_market_id.assert_called_once_with(market_id=market_id)
