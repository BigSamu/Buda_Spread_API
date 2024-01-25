import pytest
import base64
import hmac
import time
from unittest.mock import MagicMock, patch
from app.services.auth import BudaHMACAuth


@pytest.fixture
def api_key():
    return "test_api_key"


@pytest.fixture
def secret():
    return "test_secret"


@pytest.fixture
def auth_instance(api_key, secret):
    return BudaHMACAuth(api_key, secret)


class TestBudaHMACAuth:
    def test_buda_hmac_auth_init_correctly(self, auth_instance, api_key, secret):
        assert auth_instance.api_key == api_key
        assert auth_instance.secret == secret

    @patch("app.services.auth.time")  # Corrected to the actual module name
    def test_get_nonce_method_return_correct_nonce(self, mock_time, auth_instance):
        mock_time.time.return_value = 1234567
        expected_nonce = str(int(1234567 * 1e6))
        assert auth_instance.get_nonce() == expected_nonce

    def test_sign_method_sign_correctly_a_get_request(self, auth_instance):
        mock_request = MagicMock()
        mock_request.method = "GET"
        mock_request.path_url = "/test"
        mock_request.body = None

        nonce = "1234567890"
        signature = auth_instance.sign(mock_request, nonce)

        # Create expected signature
        expected_msg = f"GET /test {nonce}"
        expected_signature = hmac.new(
            key=auth_instance.secret.encode(),
            msg=expected_msg.encode(),
            digestmod="sha384",
        ).hexdigest()

        assert signature == expected_signature

    def test_sign_method_signs_correctly_a_post_request_with_body(self, auth_instance):
        # Create a mock request with a body
        mock_request = MagicMock()
        mock_request.method = "POST"
        mock_request.path_url = "/test"
        mock_request.body = b"body content"

        nonce = "1234567890"
        signature = auth_instance.sign(mock_request, nonce)

        # Create expected signature including the encoded body
        encoded_body = base64.b64encode(mock_request.body).decode()
        expected_msg = f"POST /test {encoded_body} {nonce}"
        expected_signature = hmac.new(
            key=auth_instance.secret.encode(),
            msg=expected_msg.encode(),
            digestmod="sha384",
        ).hexdigest()

        assert signature == expected_signature

    def test_call_method_modifies_correctly_get_request(self, auth_instance):
        mock_request = MagicMock()
        mock_request.method = "GET"
        mock_request.path_url = "/test"
        mock_request.body = None
        mock_request.headers = {}  # Initialize headers as an empty dict

        modified_request = auth_instance(mock_request)

        assert "X-SBTC-APIKEY" in modified_request.headers
        assert "X-SBTC-NONCE" in modified_request.headers
        assert "X-SBTC-SIGNATURE" in modified_request.headers
        assert modified_request.headers["X-SBTC-APIKEY"] == auth_instance.api_key
