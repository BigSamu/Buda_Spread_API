import pytest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from pydantic import ValidationError
from requests import Response, HTTPError

from app.main import app
from app.services.markets import MarketService
from app.services.tickers import TickerService

from config import settings
from config import (
    SAMPLE_MARKETS_DATA,
    SAMPLE_MARKETS_DATA_MISSING_MARKET_ID,
    SAMPLE_TICKER_DATA_MARKET_1,
    SAMPLE_TICKER_DATA_MARKET_2,
    SAMPLE_TICKER_DATA_MARKET_3,
    SAMPLE_TICKER_DATA_MARKET_1_INVALID_DATA,
    SAMPLE_TICKER_DATA_MARKET_2_MISSING_FIELD,
    SAMPLE_TICKER_DATA_MARKET_3_INVALID_DATAT_AND_MISSING_FIELD,
    SAMPLE_TICKERS_DATA_SET,
    SAMPLE_TICKERS_DATA_SET_INVALID_VALUE,
    SAMPLE_TICKERS_DATA_SET_MISSING_FIELD,
    SAMPLE_TICKERS_DATA_SET_INVALID_VALUE_AND_MISSING_FIELD,
)

client = TestClient(app)


# Function to return different ticker data based on market ID
def _get_ticker_data_mock(market_id: str):
    if market_id not in SAMPLE_TICKERS_DATA_SET:
        response = MagicMock(status_code=404)
        raise HTTPError("Market not found", response=response)
    return SAMPLE_TICKERS_DATA_SET[market_id]


def _get_ticker_data_mock_invalid_value(market_id: str):
    return SAMPLE_TICKERS_DATA_SET_INVALID_VALUE[market_id]


def _get_ticker_data_mock_missing_field(market_id: str):
    return SAMPLE_TICKERS_DATA_SET_MISSING_FIELD[market_id]


def _get_ticker_data_mock_invalid_value_and_missing_field(market_id: str):
    return SAMPLE_TICKERS_DATA_SET_INVALID_VALUE_AND_MISSING_FIELD[market_id]


def _raise_http_error(detail: str, status_code: int):
    def error_raiser(*args, **kwargs):
        response = MagicMock(status_code=status_code)
        raise HTTPError(detail, response=response)

    return error_raiser


class TestGetAllSpreads:
    @patch.object(MarketService, "get_all", return_value=SAMPLE_MARKETS_DATA)
    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_get_ticker_data_mock
    )
    def test_get_spreads_from_all_markets_succeeds(
        self,
        mock_get_one_ticker_by_market_id,
        mock_get_all_markets,
    ):
        # Count the number of markets
        number_of_markets = len(SAMPLE_MARKETS_DATA["markets"])

        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/spreads")

        # Check if MarketService.get_all was called once
        mock_get_all_markets.assert_called_once()

        # Check if TickerService.get_one_by_market_id was called for each market
        assert mock_get_one_ticker_by_market_id.call_count == number_of_markets

        # Validate the response
        assert response.status_code == 200
        spreads = response.json()
        assert len(spreads) == number_of_markets

        # Validate each market spread
        for spread in spreads:
            assert "min_ask" in spread
            assert "value" in spread
            assert "market_id" in spread
            assert "max_bid" in spread

    @patch.object(
        MarketService,
        "get_all",
        return_value=SAMPLE_MARKETS_DATA_MISSING_MARKET_ID,
    )
    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_get_ticker_data_mock
    )
    def test_get_spreads_from_all_markets_fails_with_invalid_market_data(
        self, mock_get_one_ticker_by_market_id, mock_get_all_markets
    ):

        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/spreads")

        # Check if MarketService.get_all was called once
        mock_get_all_markets.assert_called_once()
        # Check if TickerService.get_one_by_market_id was called at least once
        mock_get_one_ticker_by_market_id.assert_called()

        # Validate the response for unprocessable entity
        assert response.status_code == 404
        error_response = response.json()
        assert "detail" in error_response

    @pytest.mark.parametrize(
        "side_effect",
        [
            _get_ticker_data_mock_invalid_value,
            _get_ticker_data_mock_missing_field,
            _get_ticker_data_mock_invalid_value_and_missing_field,
        ],
    )
    @patch.object(MarketService, "get_all", return_value=SAMPLE_MARKETS_DATA)
    @patch.object(TickerService, "get_one_by_market_id")
    def test_get_spreads_from_all_markets_fails_with_invalid_ticker_data(
        self, mock_get_one_ticker_by_market_id, mock_get_all_markets, side_effect
    ):
        # Set the side effect for the mock_get_one_ticker_by_market_id
        mock_get_one_ticker_by_market_id.side_effect = side_effect

        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/spreads")

        # Check if MarketService.get_all was called once
        mock_get_all_markets.assert_called_once()
        # Check TickerService.get_one_by_market_id was called at least once
        mock_get_one_ticker_by_market_id.assert_called()

        # Validate the response for unprocessable entity
        assert response.status_code == 422
        error_response = response.json()

    @patch.object(
        MarketService,
        "get_all",
        side_effect=_raise_http_error(detail="Internal Server Error", status_code=500),
    )
    @patch.object(TickerService, "get_one_by_market_id")
    def test_get_spreads_from_all_markets_fails_with_internal_server_error_from_markets_service(
        self, mock_get_one_ticker_by_market_id, mock_get_all_markets
    ):
        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/spreads")

        # Check if MarketService.get_all was called once
        mock_get_all_markets.assert_called_once()
        # Check if TickerService.get_one_by_market_id was not called
        mock_get_one_ticker_by_market_id.assert_not_called()

        # Validate the response for internal server error
        assert response.status_code == 500
        error_response = response.json()
        assert "detail" in error_response
        assert (
            error_response["detail"]
            == "An unexpected error occurred: HTTPError: Internal Server Error"
        )

    @patch.object(MarketService, "get_all", return_value=SAMPLE_MARKETS_DATA)
    @patch.object(
        TickerService,
        "get_one_by_market_id",
        side_effect=_raise_http_error(detail="Internal Server Error", status_code=500),
    )
    def test_get_all_spreads_fails_with_internal_server_error_from_tickers_service(
        self, mock_get_one_ticker_by_market_id, mock_get_all_markets
    ):
        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/spreads")

        # Check MarketService.get_all was called once
        mock_get_all_markets.assert_called_once()
        # Check TickerService.get_one_by_market_id was called at least once
        mock_get_one_ticker_by_market_id.assert_called()

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
        TickerService, "get_one_by_market_id", return_value=SAMPLE_TICKER_DATA_MARKET_1
    )
    def test_get_spread_by_market_id_succeeds(self, mock_get_one_ticker_by_market_id):
        # Making the request
        market_id = "market_1"
        response = client.get(f"{settings.API_URL_PREFIX}/spreads/{market_id}")

        # Check TickerService.get_one_by_market_id was called once with specific argument
        mock_get_one_ticker_by_market_id.assert_called_once_with(market_id=market_id)

        # Validate the response
        assert response.status_code == 200
        spread = response.json()

        # Add more assertions for spread fields
        assert spread["market_id"] == market_id
        assert spread["value"] == "100.000000"
        assert spread["max_bid"] == "900.000000"
        assert spread["min_ask"] == "1,000.000000"

    @patch.object(
        TickerService,
        "get_one_by_market_id",
        side_effect=_raise_http_error(detail="Market not found", status_code=404),
    )
    def test_get_spread_by_market_id_fails_with_not_found_error(
        self, mock_get_one_ticker_by_market_id
    ):
        # Making the request
        market_id = "unknown_market"
        response = client.get(f"{settings.API_URL_PREFIX}/spreads/{market_id}")

        # Check TickerService.get_one_by_market_id was called once with specific argument
        mock_get_one_ticker_by_market_id.assert_called_once_with(market_id=market_id)

        # Validate the response for not found error
        assert response.status_code == 404
        error_response = response.json()
        assert "detail" in error_response
        assert error_response["detail"] == f"Market with id '{market_id}' not found"

    @pytest.mark.parametrize(
        "market_id, malformed_ticker",
        [
            ("market_1", SAMPLE_TICKER_DATA_MARKET_1_INVALID_DATA),
            ("market_2", SAMPLE_TICKER_DATA_MARKET_2_MISSING_FIELD),
            ("market_3", SAMPLE_TICKER_DATA_MARKET_3_INVALID_DATAT_AND_MISSING_FIELD),
        ],
    )
    @patch.object(TickerService, "get_one_by_market_id")
    def test_get_spread_by_market_id_fails_with_invalid_ticker_data(
        self, mock_get_one_ticker_by_market_id, market_id, malformed_ticker
    ):
        # Set the side effect for the mock_get_one_ticker_by_market_id
        mock_get_one_ticker_by_market_id.return_value = malformed_ticker

        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/spreads/{market_id}")

        # Check TickerService.get_one_by_market_id was called once with specific argument
        mock_get_one_ticker_by_market_id.assert_called_once_with(market_id=market_id)

        # Validate the response for unprocessable entity
        assert response.status_code == 422
        error_response = response.json()

    @patch.object(
        TickerService,
        "get_one_by_market_id",
        side_effect=_raise_http_error(detail="Internal Server Error", status_code=500),
    )
    def test_get_spread_by_market_id_internal_server_error(
        self, mock_get_one_ticker_by_market_id
    ):
        # Making the request
        market_id = "market_1"
        response = client.get(f"{settings.API_URL_PREFIX}/spreads/{market_id}")

        # Check TickerService.get_one_by_market_id was called once with specific argument
        mock_get_one_ticker_by_market_id.assert_called_once_with(market_id=market_id)

        # Validate the response for internal server error
        assert response.status_code == 500
        error_response = response.json()
        assert "detail" in error_response
        assert (
            error_response["detail"]
            == "An unexpected error occurred: HTTPError: Internal Server Error"
        )
