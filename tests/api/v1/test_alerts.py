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
    SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    SAMPLE_SPREAD_ALERT_EMPTY,
)

client = TestClient(app)


# Function to return different ticker data based on market ID
def _get_ticker_data_mock(market_id: str):
    """Return different ticker data based on the market ID."""
    return SAMPLE_TICKERS_DATA_SET[market_id]


class TestCompareAlertWithAllMarkets:

    @patch.object(MarketService, "get_all", return_value=SAMPLE_MARKETS_DATA)
    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_get_ticker_data_mock
    )
    @patch(
        "app.api.v1.alerts.spread_alert",
        new_callable=lambda: SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    )
    def test_compare_alert_with_all_markets_succeeds(
        self, mock_spread_alert, mock_get_one_ticker_by_market_id, mock_get_all_markets
    ):

        # Count the number of markets
        number_of_markets = len(SAMPLE_MARKETS_DATA["markets"])

        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/alerts")

        # Check if MarketService.get_all was called once
        mock_get_all_markets.assert_called_once()

        # Check if TickerService.get_one_by_market_id was called for each market
        assert mock_get_one_ticker_by_market_id.call_count == number_of_markets

        # Validate the response
        assert response.status_code == 200
        alerts = response.json()
        assert len(alerts) == number_of_markets

        # Validate each alert item has the expected fields
        for market_id, alert in alerts.items():
            assert "market_id" in alert
            assert "spread_value" in alert
            assert "alert_value" in alert
            assert "is_greater" in alert
            assert "is_less" in alert
            assert "message" in alert

    @patch.object(MarketService, "get_all", return_value=SAMPLE_MARKETS_DATA)
    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_get_ticker_data_mock
    )
    @patch(
        "app.api.v1.alerts.spread_alert", new_callable=lambda: SAMPLE_SPREAD_ALERT_EMPTY
    )
    def test_compare_alert_with_all_markets_fails_with_spread_alert_value_empty(
        self, mock_spread_alert, mock_get_one_ticker_by_market_id, mock_get_all_markets
    ):

        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/alerts")

        # Check if MarketService.get_all was not called
        mock_get_all_markets.assert_not_called()
        # Check if TickerService.get_one_by_market_id was not called
        mock_get_one_ticker_by_market_id.assert_not_called()

        # Validate the response
        assert response.status_code == 404
        error = response.json()
        assert error["detail"] == "Spread Alert not set yet. Please set one first."

    @patch.object(
        MarketService, "get_all", return_value=SAMPLE_MARKETS_DATA_MISSING_MARKET_ID
    )
    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_get_ticker_data_mock
    )
    @patch(
        "app.api.v1.alerts.spread_alert", new_callable=lambda: SAMPLE_SPREAD_ALERT_EMPTY
    )
    def test_compare_alert_with_all_markets_fails_with_spread_alert_value_empty(
        self, mock_spread_alert, mock_get_one_ticker_by_market_id, mock_get_all_markets
    ):
        pass
