# Import the functions to be tested
import pytest
from app.utils import calculate_spread, compare_spread_with_alert_value

class TestCalculateSpread:
    def test_calculate_spread_succeeds(self):
        # Test successful spread calculation
        result = calculate_spread("15.0", "10.0", "market1")
        assert result["min_ask"] == 15.0
        assert result["max_bid"] == 10.0
        assert result["value"] == 5.0  # 15.0 - 10.0
        assert result["market_id"] == "market1"

    def test_calculate_spread_with_invalid_min_ask_value_fails(self):
        # Test with invalid min_ask value
        with pytest.raises(ValueError) as excinfo:
            calculate_spread("invalid", "10.0", "market2")
        assert "Error calculating spread for market market2" in str(excinfo.value)

    def test_calculate_spread_with_invalid_max_bid_value_fails(self):
        # Test with invalid max_bid value
        with pytest.raises(ValueError) as excinfo:
            calculate_spread("15.0", "invalid", "market3")
        assert "Error calculating spread for market market3" in str(excinfo.value)

    def test_calculate_spread_with_invalid_min_ask_and_max_bid_values_fails(self):
        # Test with both min_ask and max_bid invalid
        with pytest.raises(ValueError) as excinfo:
            calculate_spread("invalid_min", "invalid_max", "market4")
        assert "Error calculating spread for market market4" in str(excinfo.value)

class TestCompareSpreadWithAlertValue:
    """
    Test the compare_spread_with_alert_value function.
    """
    def test_compare_spread_with_greater_spread_value_than_alert_value_succeeds(self):
        # Test when spread_value is greater than alert_value
        result = compare_spread_with_alert_value("10.0", "5.0", "market1")
        assert result["is_greater"] is True
        assert result["is_less"] is False
        assert result["message"] == "Spread for market market1 is GREATER than the alert value by 5.00. Spread Value: 10.00, Alert Value: 5.00"

    def test_compare_spread_with_lesser_spread_value_than_alert_value_succeeds(self):
        # Test when spread_value is less than alert_value
        result = compare_spread_with_alert_value("5.0", "10.0", "market2")
        assert result["is_greater"] is False
        assert result["is_less"] is True
        assert result["message"] == "Spread for market market2 is LESS than the alert value by 5.00. Spread Value: 5.00, Alert Value: 10.00"

    def test_compare_spread_with_equal_spread_value_than_alert_value_succeeds(self):
        # Test when spread_value is equal to alert_value
        result = compare_spread_with_alert_value("7.0", "7.0", "market3")
        assert result["is_greater"] is False
        assert result["is_less"] is False
        assert result["message"] == "Spread is for market market3 is EQUAL to the alert value. Spread Value: 7.00, Alert Value: 7.00"

    def test_compare_spread_with_invalid_spread_value_fails(self):
        # Test with an invalid spread_value
        with pytest.raises(ValueError) as excinfo:
            compare_spread_with_alert_value("invalid", "5.0", "market1")
        assert "Error calculating spread for market market1" in str(excinfo.value)

    def test_compare_spread_with_invalid_alert_value_fails(self):
        # Test with an invalid alert_value
        with pytest.raises(ValueError) as excinfo:
            compare_spread_with_alert_value("10.0", "invalid", "market2")
        assert "Error calculating spread for market market2" in str(excinfo.value)

    def test_compare_spread_with_invalid_spread_and_alert_values_fails(self):
        # Test with both spread_value and alert_value invalid
        with pytest.raises(ValueError) as excinfo:
            compare_spread_with_alert_value("invalid", "also_invalid", "market3")
        assert "Error calculating spread for market market3" in str(excinfo.value)
