from typing import Dict
from app.services import buda_api


def calculate_spread(ticker: Dict[str, str]) -> Dict[str, str]:
    """
    Calculate the spread for a given market ID.

    **Args:**

        - ticker_dict (Dict[str, str]): A dictionary containing the following ticker data:
            - 'min_ask': A list containing the minimum ask price and currency for the market, e.g., ["30000.01", "ARS"].
            - 'max_bid': A list containing the maximum bid price and currency for the market, e.g., ["29990.0", "ARS"].
            - 'market_id': The unique identifier of the market, e.g., "BCH-ARS".

    **Returns:**

        current_spread (Dict[str, str]): A dictionary containing the following:

            - 'min_ask': The minimum ask price for the market.
            - 'max_bid': The maximum bid price for the market.
            - 'value': The calculated spread value (min_ask - max_bid) for the market.
            - 'market_id': The unique identifier of the market.

    **Raises:**

        A ValueError will be raised if the spread value or alert value cannot be converted to a float.
    """

    try:
        min_ask = (float)(ticker["min_ask"][0])
        max_bid = (float)(ticker["max_bid"][0])
        current_spread = {
            "min_ask": min_ask,
            "max_bid": max_bid,
            "value": min_ask - max_bid,
            "market_id": ticker["market_id"],
        }
        return current_spread
    except ValueError as e:
        raise ValueError(
            f"Error calculating spread for market {ticker['market_id']}: {str(e)}"
        )


def compare_spread_with_alert_value(
    spread_value: str, alert_value: str, market_id: str
) -> Dict[str, str]:
    """
    Compare the spread value with the alert value.

    **Args:**

        - spread_value (str): The spread value to be compared.
        - alert_value (str): The alert value against which the spread value is compared.
        - market_id (str): The unique identifier of the market for which the spread value is compared.

    **Returns:**

        alert (Dict[str, str]): A dictionary containing the following:

            - market_id (str): The unique identifier of the market.
            - spread_value (str): The calculated spread value for the market.
            - alert_value (str): The value of the spread alert.
            - is_greater (bool): A boolean indicating whether the spread is greater than the alert value.
            - is_less (bool): A boolean indicating whether the spread is less than the alert value.
            - message (str): A string message indicating the status of the spread alert. Possible messages include:

                - "Spread is GREATER than the alert value."
                - "Spread is LESS than the alert value."
                - "Spread is EQUAL to the alert value."

    **Raises:**

        - ValueError: if spread value or alert value cannot be converted to a float.
        - KeyError: if spread value or alert value is not found in the input dictionary.
    """
    try:
        spread_value = (float)(spread_value)
        alert_value = (float)(alert_value)
        diff_spread_alert_value = spread_value - alert_value

        spread_value_formatted = "{:,.2f}".format(spread_value)
        alert_value_formatted = "{:,.2f}".format(alert_value)
        diff_spread_alert_value_formatted = "{:,.2f}".format(
            abs(diff_spread_alert_value)
        )

        if diff_spread_alert_value > 0:
            alert_message = f"Spread for market {market_id} is GREATER than the alert value by {diff_spread_alert_value_formatted}."
        elif diff_spread_alert_value < 0:
            alert_message = f"Spread for market {market_id} is LESS than the alert value by {diff_spread_alert_value_formatted}."
        else:
            alert_message = (
                f"Spread is for market {market_id} is EQUAL to the alert value."
            )

        alert_message += f" Spread Value: {spread_value_formatted}, Alert Value: {alert_value_formatted}"

        alert = {
            "market_id": market_id,
            "spread_value": spread_value_formatted,
            "alert_value": alert_value_formatted,
            "is_greater": diff_spread_alert_value > 0,
            "is_less": diff_spread_alert_value < 0,
            "message": alert_message,
        }
        return alert

    except ValueError as e:
        raise ValueError(f"Error formatting spread for market {market_id}: {str(e)}")
