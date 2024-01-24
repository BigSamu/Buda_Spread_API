import pytest
from app.utils import format_current_spread


class TestFormatCurrentSpread:
    def test_format_current_spread_succeeds(self):
        # Test successful formatting of spread dictionary
        input_current_spread = {
            "min_ask": 1234.56789,
            "max_bid": 987.65432,
            "value": 246.91357,
            "market_id": "market1",
        }
        result = format_current_spread(input_current_spread)
        assert result["min_ask"] == "1,234.567890"
        assert result["max_bid"] == "987.654320"
        assert result["value"] == "246.913570"
        assert result["market_id"] == "market1"

    def test_format_current_spread_with_invalid_min_ask_value_fails(self):
        # Test with invalid value (non-numeric) in spread dictionary
        invalid_current_spread = {
            "min_ask": "invalid",
            "max_bid": 987.65432,
            "value": 246.91357,
            "market_id": "market2",
        }
        with pytest.raises(ValueError) as excinfo:
            format_current_spread(invalid_current_spread)
        assert "Error formatting spread for market market2" in str(excinfo.value)

    def test_format_current_spread_with_invalid_max_bid_value_fails(self):
        # Test with invalid value (non-numeric) in spread dictionary
        invalid_current_spread = {
            "min_ask": 1234.56789,
            "max_bid": "invalid",
            "value": 246.91357,
            "market_id": "market3",
        }
        with pytest.raises(ValueError) as excinfo:
            format_current_spread(invalid_current_spread)
        assert "Error formatting spread for market market3" in str(excinfo.value)

    def test_format_current_spread_with_invalid_spread_value_fails(self):
        # Test with invalid value (non-numeric) in spread dictionary
        invalid_current_spread = {
            "min_ask": 1234.56789,
            "max_bid": 987.65432,
            "value": "invalid",
            "market_id": "market3",
        }
        with pytest.raises(ValueError) as excinfo:
            format_current_spread(invalid_current_spread)
        assert "Error formatting spread for market market3" in str(excinfo.value)

    def test_format_current_spread_with_missing_key_fails(self):
        # Test with missing key in spread dictionary
        invalid_current_spread = {
            "min_ask": 1234.56789,
            # Missing max_bid
            "value": 246.91357,
            "market_id": "market3",
        }
        with pytest.raises(KeyError) as excinfo:
            format_current_spread(invalid_current_spread)
        assert "Error formatting spread for market market3" in str(excinfo.value)
