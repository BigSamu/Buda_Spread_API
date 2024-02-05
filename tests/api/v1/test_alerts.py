import pytest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from pydantic import ValidationError
from requests import Response, HTTPError

from app.main import app
from app.services.markets import MarketService
from app.services.tickers import TickerService

from app.api.v1.alerts import spread_alert

from config import settings
from config import (
    SAMPLE_MARKETS_DATA,
    SAMPLE_MARKETS_DATA_MISSING_MARKET_ID,
    SAMPLE_TICKER_DATA_MARKET_1_INVALID_DATA,
    SAMPLE_TICKER_DATA_MARKET_2_MISSING_FIELD,
    SAMPLE_TICKER_DATA_MARKET_3_INVALID_DATA_AND_MISSING_FIELD,
    SAMPLE_TICKERS_DATA_SET,
    SAMPLE_TICKERS_DATA_SET_INVALID_VALUE,
    SAMPLE_TICKERS_DATA_SET_MISSING_FIELD,
    SAMPLE_TICKERS_DATA_SET_INVALID_VALUE_AND_MISSING_FIELD,
    SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    SAMPLE_SPREAD_ALERT_EMPTY,
)

client = TestClient(app)


# Functions to return different ticker data based on market ID
def _get_tickers_data_set(market_id: str):
    if market_id not in SAMPLE_TICKERS_DATA_SET:
        response = MagicMock(status_code=404)
        raise HTTPError("Market not found", response=response)
    return SAMPLE_TICKERS_DATA_SET[market_id]

def _get_tickers_data_set_with_invalid_value_sample(market_id: str):
    return SAMPLE_TICKERS_DATA_SET_INVALID_VALUE[market_id]

def _get_tickers_data_set_with_missing_field_sample(market_id: str):
    return SAMPLE_TICKERS_DATA_SET_MISSING_FIELD[market_id]

def _get_tickers_data_set_with_invalid_value_and_missing_field_sample(market_id: str):
    return SAMPLE_TICKERS_DATA_SET_INVALID_VALUE_AND_MISSING_FIELD[market_id]

# Aux function to raise an HTTP error
def _raise_http_error(detail: str, status_code: int):
    def error_raiser(*args, **kwargs):
        response = MagicMock(status_code=status_code)
        raise HTTPError(detail, response=response)
    return error_raiser

class TestCompareAlertWithAllMarkets:

    @patch.object(MarketService, "get_all", return_value=SAMPLE_MARKETS_DATA)
    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_get_tickers_data_set
    )
    @patch.dict(
        "app.api.v1.alerts.spread_alert", SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP
    )
    def test_compare_alert_with_all_markets_succeeds(
        self, mock_get_one_ticker_by_market_id, mock_get_all_markets
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
        TickerService, "get_one_by_market_id", side_effect=_get_tickers_data_set
    )
    @patch.dict(
        "app.api.v1.alerts.spread_alert", SAMPLE_SPREAD_ALERT_EMPTY
    )
    def test_compare_alert_with_all_markets_fails_with_spread_alert_value_empty(
        self, mock_get_one_ticker_by_market_id, mock_get_all_markets
    ):

        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/alerts")

        # Check MarketService.get_all was not called
        mock_get_all_markets.assert_not_called()
        # Check TickerService.get_one_by_market_id was not called
        mock_get_one_ticker_by_market_id.assert_not_called()

        # Validate the response
        assert response.status_code == 404
        error = response.json()
        assert error["detail"] == "Spread Alert not set yet. Please set one first."

    @patch.object(
        MarketService, "get_all", return_value=SAMPLE_MARKETS_DATA_MISSING_MARKET_ID
    )
    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_get_tickers_data_set
    )
    @patch.dict(
        "app.api.v1.alerts.spread_alert", SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    )
    def test_compare_alert_with_all_markets_fails_with_invalid_market_data(
        self, mock_get_one_ticker_by_market_id, mock_get_all_markets
    ):
        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/alerts")

        # Check if MarketService.get_all was called once
        mock_get_all_markets.assert_called_once()

        # Check if TickerService.get_one_by_market_id was called at least once
        mock_get_one_ticker_by_market_id.assert_called()

        # Validate the response for not found error
        assert response.status_code == 404
        error = response.json()
        assert error["detail"] == "Market not found"

    @pytest.mark.parametrize(
        "side_effect",
        [
            _get_tickers_data_set_with_invalid_value_sample,
            _get_tickers_data_set_with_missing_field_sample,
            _get_tickers_data_set_with_invalid_value_and_missing_field_sample,
        ],
    )
    @patch.object(MarketService, "get_all", return_value=SAMPLE_MARKETS_DATA)
    @patch.object(TickerService, "get_one_by_market_id")
    @patch.dict(
        "app.api.v1.alerts.spread_alert", SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    )
    def test_compare_alert_with_all_markets_fails_with_invalid_ticker_data(
        self, mock_get_one_ticker_by_market_id, mock_get_all_markets, side_effect
    ):
        # Set the side effect for the mock_get_one_ticker_by_market_id
        mock_get_one_ticker_by_market_id.side_effect = side_effect

        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/alerts")

        # Check if MarketService.get_all was called once
        mock_get_all_markets.assert_called_once()

        # Check if TickerService.get_one_by_market_id was called at least once
        mock_get_one_ticker_by_market_id.assert_called()

        # Validate the response for unproucessable entity error
        assert response.status_code == 422
        error_response = response.json()
        assert "detail" in error_response


    @patch.object(
        MarketService,
        "get_all",
        side_effect=_raise_http_error(detail="Internal Server Error", status_code=500),
    )
    @patch.object(TickerService, "get_one_by_market_id")
    @patch.dict(
        "app.api.v1.alerts.spread_alert", SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    )
    def test_compare_alert_with_all_markets_fails_with_internal_server_error_from_markets_service(
        self, mock_get_one_ticker_by_market_id, mock_get_all_markets
    ):
        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/alerts")

        # Check if MarketService.get_all was called once
        mock_get_all_markets.assert_called_once()

        # Check if TickerService.get_one_by_market_id was not called
        mock_get_one_ticker_by_market_id.assert_not_called()

        # Validate the response for internal server error
        assert response.status_code == 500
        error_response = response.json()
        assert "detail" in error_response
        assert (error_response["detail"] == "An unexpected error occurred: HTTPError: Internal Server Error")

    @patch.object(MarketService, "get_all", return_value=SAMPLE_MARKETS_DATA)
    @patch.object(
        TickerService,
        "get_one_by_market_id",
        side_effect=_raise_http_error(detail="Internal Server Error", status_code=500),
    )
    @patch.dict(
        "app.api.v1.alerts.spread_alert", SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    )
    def test_get_all_spreads_fails_with_internal_server_error_from_tickers_service(
        self, mock_get_one_ticker_by_market_id, mock_get_all_markets
    ):
        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/alerts")

        # Check if MarketService.get_all was called once
        mock_get_all_markets.assert_called_once()

        # Check if TickerService.get_one_by_market_id was called at least once
        mock_get_one_ticker_by_market_id.assert_called()

        # Validate the response for internal server error
        assert response.status_code == 500
        error_response = response.json()
        assert "detail" in error_response
        assert (error_response["detail"] == "An unexpected error occurred: HTTPError: Internal Server Error")

class TestCompareAlertWithOneMarket:

    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_get_tickers_data_set
    )
    @patch.dict(
        "app.api.v1.alerts.spread_alert",  SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    )
    def test_compare_alert_with_one_market_succeeds_with_spread_equal_to_alert_value(
        self, mock_get_one_ticker_by_market_id
    ):

        # Making the request
        market_id = "market_1"
        response = client.get(f"{settings.API_URL_PREFIX}/alerts/{market_id}")
        # Check if TickerService.get_one_by_market_id was called once
        mock_get_one_ticker_by_market_id.assert_called_once_with(market_id=market_id)

        # Validate the response
        assert response.status_code == 200
        alert = response.json()

        assert alert["market_id"] == market_id
        assert alert["spread_value"] == "100.00"
        assert alert["alert_value"] == "100.00"
        assert alert["is_greater"] == False
        assert alert["is_less"] == False
        assert alert["message"] == "Spread is for market market_1 is EQUAL to the alert value. Spread Value: 100.00, Alert Value: 100.00"

    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_get_tickers_data_set
    )
    @patch.dict(
        "app.api.v1.alerts.spread_alert",  SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    )
    def test_compare_alert_with_one_market_succeeds_with_spread_lesser_to_alert_value(
        self, mock_get_one_ticker_by_market_id
    ):

        # Making the request
        market_id = "market_2"
        response = client.get(f"{settings.API_URL_PREFIX}/alerts/{market_id}")
        # Check if TickerService.get_one_by_market_id was called once
        mock_get_one_ticker_by_market_id.assert_called_once_with(market_id=market_id)

        # Validate the response
        assert response.status_code == 200
        alert = response.json()

        assert alert["market_id"] == market_id
        assert alert["spread_value"] == "50.00"
        assert alert["alert_value"] == "100.00"
        assert alert["is_greater"] == False
        assert alert["is_less"] == True
        assert alert["message"] == "Spread for market market_2 is LESS than the alert value by 50.00. Spread Value: 50.00, Alert Value: 100.00"


    @patch.object(
        TickerService, "get_one_by_market_id", side_effect=_get_tickers_data_set
    )
    @patch.dict(
        "app.api.v1.alerts.spread_alert",  SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    )
    def test_compare_alert_with_one_market_succeeds_with_spread_greater_to_alert_value(
        self, mock_get_one_ticker_by_market_id
    ):

        # Making the request
        market_id = "market_3"
        response = client.get(f"{settings.API_URL_PREFIX}/alerts/{market_id}")
        # Check if TickerService.get_one_by_market_id was called once
        mock_get_one_ticker_by_market_id.assert_called_once_with(market_id=market_id)

        # Validate the response
        assert response.status_code == 200
        alert = response.json()

        assert alert["market_id"] == market_id
        assert alert["spread_value"] == "150.00"
        assert alert["alert_value"] == "100.00"
        assert alert["is_greater"] == True
        assert alert["is_less"] == False
        assert alert["message"] == "Spread for market market_3 is GREATER than the alert value by 50.00. Spread Value: 150.00, Alert Value: 100.00"

    @patch.object(
        TickerService,
        "get_one_by_market_id",
        side_effect=_raise_http_error(detail="Market not found", status_code=404),
    )
    @patch.dict(
        "app.api.v1.alerts.spread_alert",  SAMPLE_SPREAD_ALERT_EMPTY,
    )
    def test_compare_alert_with_one_market_fails_with_spread_alert_value_empty(
        self, mock_get_one_ticker_by_market_id
    ):
        # Making the request
        market_id = "market_1"
        response = client.get(f"{settings.API_URL_PREFIX}/alerts/{market_id}")

        # Check TickerService.get_one_by_market_id was not called
        mock_get_one_ticker_by_market_id.assert_not_called()

        # Validate the response for not found error
        assert response.status_code == 404
        error_response = response.json()
        assert "detail" in error_response
        assert error_response["detail"] == f"Spread Alert not set yet. Please set one first."

    @patch.object(
        TickerService,
        "get_one_by_market_id",
        side_effect=_raise_http_error(detail="Market not found", status_code=404),
    )
    @patch.dict(
        "app.api.v1.alerts.spread_alert",  SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    )
    def test_compare_alert_with_one_market_fails_with_market_not_found_error(
        self, mock_get_one_ticker_by_market_id
    ):
        # Making the request
        market_id = "unkownw_market"
        response = client.get(f"{settings.API_URL_PREFIX}/alerts/{market_id}")

        # Check TickerService.get_one_by_market_id was not called
        mock_get_one_ticker_by_market_id.assert_called_with(market_id=market_id)

        # Validate the response for not found error
        assert response.status_code == 404
        error_response = response.json()
        assert "detail" in error_response
        assert error_response["detail"] == f"Market with id 'unkownw_market' not found"

    @pytest.mark.parametrize(
        "market_id, malformed_ticker",
        [
            ("market_1", SAMPLE_TICKER_DATA_MARKET_1_INVALID_DATA),
            ("market_2", SAMPLE_TICKER_DATA_MARKET_2_MISSING_FIELD),
            ("market_3", SAMPLE_TICKER_DATA_MARKET_3_INVALID_DATA_AND_MISSING_FIELD),

        ],
    )
    @patch.object(
        TickerService,
        "get_one_by_market_id")
    @patch.dict(
        "app.api.v1.alerts.spread_alert",  SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    )
    def test_compare_alert_with_one_market_fails_with_invalid_ticker_data(
        self, mock_get_one_ticker_by_market_id, market_id, malformed_ticker
    ):
        # Set the side effect for the mock_get_one_ticker_by_market_id
        mock_get_one_ticker_by_market_id.return_value = malformed_ticker

        # Making the request
        response = client.get(f"{settings.API_URL_PREFIX}/alerts/{market_id}")

        # Check TickerService.get_one_by_market_id was called once with specific argument
        mock_get_one_ticker_by_market_id.assert_called_once_with(market_id=market_id)

        # Validate the response for unprocessable entity
        assert response.status_code == 422
        error_response = response.json()
        assert "detail" in error_response

    @patch.object(
        TickerService,
        "get_one_by_market_id",
        side_effect=_raise_http_error(detail="Internal Server Error", status_code=500),
    )
    @patch.dict(
        "app.api.v1.alerts.spread_alert",  SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP,
    )
    def test_compare_alert_with_one_market_fails_with_internal_server_error(
        self, mock_get_one_ticker_by_market_id
    ):
        # Making the request
        market_id = "market_1"
        response = client.get(f"{settings.API_URL_PREFIX}/alerts/{market_id}")

        # Check TickerService.get_one_by_market_id was called once
        mock_get_one_ticker_by_market_id.assert_called_once_with(market_id=market_id)

        # Validate the response for internal server error
        assert response.status_code == 500
        error_response = response.json()
        assert "detail" in error_response
        assert error_response["detail"] == "An unexpected error occurred: HTTPError: Internal Server Error"

class TestSetSpreadAlert:

    @patch.dict(
        "app.api.v1.alerts.spread_alert",  SAMPLE_SPREAD_ALERT_EMPTY
    )
    def test_set_spread_alert_succeeds(self):

        # Validate initial status of spread_alert
        assert spread_alert["value"] == None

        # Making the request
        response = client.post(
            f"{settings.API_URL_PREFIX}/alerts",
            json={"value": "100.00"},
        )

        # Validate the response and later status of spread_alert
        assert response.status_code == 200
        message = response.json()
        assert message == {"message": "Alert set successfully. Alert value: 100.00"}
        assert spread_alert["value"] == 100.00

    @patch.dict(
        "app.api.v1.alerts.spread_alert",  SAMPLE_SPREAD_ALERT_EMPTY
    )
    def test_set_spread_alert_fails_with_invalid_value(self):

        # Validate initial status of spread_alert
        assert spread_alert["value"] == None

        # Making the request
        response = client.post(
            f"{settings.API_URL_PREFIX}/alerts",
            json={"value": "xx"},
        )

        # Validate the response and later status of spread_alert
        assert response.status_code == 422
        assert spread_alert["value"] == None

    @patch.dict(
        "app.api.v1.alerts.spread_alert",  SAMPLE_SPREAD_ALERT_EMPTY
    )
    def test_set_spread_alert_fails_with_missing_value(self):

            # Validate initial status of spread_alert
            assert spread_alert["value"] == None

            # Making the request
            response = client.post(
                f"{settings.API_URL_PREFIX}/alerts",
                json={},
            )

            # Validate the response and later status of spread_alert
            assert response.status_code == 422
            assert spread_alert["value"] == None
