import pytest
import requests
from unittest.mock import MagicMock, patch
from requests.exceptions import RequestException

from config import settings
from app.services.base_api_client import BaseAPIClient
from app.services.auth import BudaHMACAuth


@pytest.fixture
def base_api_client():
    return BaseAPIClient()


class TestBaseAPIClient:
    def test_base_client_init_correctly(self, base_api_client):
        assert base_api_client.base_url == settings.BUDA_API_URL

    @patch.object(requests, "get")
    @patch("app.services.base_api_client.BudaHMACAuth")
    def test_base_api_client_get_request_succeeds(
        self, mock_buda_hmac_auth_class, mock_get, base_api_client
    ):
        # Mock the BudaHMACAuth class and instance
        mock_buda_hmac_auth_instance = MagicMock()
        mock_buda_hmac_auth_class.return_value = mock_buda_hmac_auth_instance

        # Define a sample response for the mock GET request
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {"key": "value"}

        # Call the get method with a mock path
        response = base_api_client._get("some_path")

        # Assert that requests.get was called with the expected URL
        mock_get.assert_called_once_with(
            f"{settings.BUDA_API_URL}/some_path", auth=mock_buda_hmac_auth_instance
        )

        # Assert that the response data matches the expected data
        assert response == {"key": "value"}

    @patch.object(requests, "get")
    @patch("app.services.base_api_client.BudaHMACAuth")
    def test_base_api_client_get_request_fails(
        self, mock_buda_hmac_auth_class, mock_get, base_api_client
    ):
        # Mock the BudaHMACAuth class and instance
        mock_buda_hmac_auth_instance = MagicMock()
        mock_buda_hmac_auth_class.return_value = mock_buda_hmac_auth_instance

        # Define a sample response for the mock GET request
        mock_get.return_value.ok = False
        mock_get.return_value.raise_for_status.side_effect = RequestException

        # Call the get method with a mock path
        with pytest.raises(RequestException):
            response = base_api_client._get("some_path")

            # Assert that requests.get was called with the expected URL
            mock_get.assert_called_once_with(
                f"{settings.BUDA_API_URL}/some_path", auth=mock_buda_hmac_auth_instance
            )
