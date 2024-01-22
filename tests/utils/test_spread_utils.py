# Import the function to be tested
from app.utils.spread_utils import calculate_spread, compare_spread_with_alert_value
# Write test cases
def test_compare_spread_greater():
    # Test when spread_value is greater than alert_value
    result = compare_spread_with_alert_value(10.0, "5.0", "market1")
    assert result["is_greater"] is True
    assert result["is_less"] is False
    assert result["message"] == "Spread for market market1 is GREATER than the alert value by 5.00000000. Spread: 10.00000000, Alert: 5.00000000"

def test_compare_spread_less():
    # Test when spread_value is less than alert_value
    result = compare_spread_with_alert_value(5.0, "10.0", "market2")
    assert result["is_greater"] is False
    assert result["is_less"] is True
    assert result["message"] == "Spread for market market2 is LESS than the alert value by 5.00000000. Spread: 5.00000000, Alert: 10.00000000"

def test_compare_spread_equal():
    # Test when spread_value is equal to alert_value
    result = compare_spread_with_alert_value(7.0, "7.0", "market3")
    assert result["is_greater"] is False
    assert result["is_less"] is False
    assert result["message"] == "Spread is for market market3 is EQUAL to the alert value. Spread: 7.00000000, Alert: 7.00000000"
