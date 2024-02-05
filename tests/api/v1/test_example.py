from fastapi.testclient import TestClient
from unittest.mock import patch
from requests.exceptions import HTTPError
from app.main import app  # Adjust the import path to your FastAPI app's actual location

client = TestClient(app)


def mock_get_all_markets():
    """Simulates an HTTPError being raised by the markets service."""
    response_mock = HTTPError()
    response_mock.response = type("obj", (object,), {"status_code": 404})
    raise response_mock


@patch("app.services.buda_api.markets.get_all", side_effect=mock_get_all_markets)
def test_get_all_spreads_with_http_error(mock_get_all):
    response = client.get("/spreads")  # Adjust the URL based on your route
    assert response.status_code == 404
