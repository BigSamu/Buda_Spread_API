# import pytest
# from unittest.mock import MagicMock, patch

# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)


# class TestGetAllSpreads:
#     @patch("app.api.v1.spreads.buda_api")
#     def test_get_all_spreads_success(self, mock_buda_api):
#         # Arrange
#         mock_buda_api.markets.get_all.return_value = {
#             "markets": [
#                 {"id": "btc-clp"},
#                 {"id": "eth-clp"},
#                 {"id": "eth-btc"},
#             ]
#         }
#         mock_buda_api.tickers.get_one_by_market_id.side_effect = [
#             {"ticker": {"max_bid": "10000000", "min_ask": "9000000"}},
#             {"ticker": {"max_bid": "1000000", "min_ask": "900000"}},
#             {"ticker": {"max_bid": "10000", "min_ask": "9000"}},
#         ]
#         expected_response = [
#             {
#                 "max_bid": "10000000",
#                 "min_ask": "9000000",
#                 "spread_value": "1000000",
#                 "market_id": "btc-clp",
#             },
#             {
#                 "max_bid": "1000000",
#                 "min_ask": "900000",
#                 "spread_value": "100000",
#                 "market_id": "eth-clp",
#             },
#             {
#                 "max_bid": "10000",
#                 "min_ask": "9000",
#                 "spread_value": "1000",
#                 "market_id": "eth-btc",
#             },
#         ]

#         # Act
#         response = client.get("/api/v1/spreads")

#         # Assert
#         assert response.status_code == 200
#         assert response.json() == expected_response

#     @patch("app.api.v1.spreads.buda_api")
#     def test_get_all_spreads_error(self, mock_buda_api):
#         # Arrange
#         mock_buda_api.markets.get_all.side_effect = Exception("Error")
#         expected_response = {"detail": "An unexpected error occurred: Exception: Error"}

#         # Act
#         response = client.get("/api/v1/spreads")

#         # Assert
#         assert response.status_code == 500
#         assert response.json() == expected_response
