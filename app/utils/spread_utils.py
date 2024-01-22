from typing import Dict
from app.services import buda_api


def calculate_spread(market_id: str) -> Dict[str, str]:
    """
    Calculate the spread for a given market ID.

    **Args:**

        market_id (str): The unique identifier of the market for which the spread is calculated.

    **Returns:**

        Dict[str, str]: A dictionary containing the following:

            - 'min_ask': The minimum ask price for the market.
            - 'max_bid': The maximum bid price for the market.
            - 'value': The calculated spread value (min_ask - max_bid) for the market.
            - 'market_id': The unique identifier of the market.

    **Raises:**

        Any exceptions raised during the API request or data processing will be propagated.
    """

    ticker = buda_api.tickers.get_one_by_market_id(market_id=market_id)["ticker"]
    min_ask = (float)(ticker["min_ask"][0])
    max_bid = (float)(ticker["max_bid"][0])
    value = min_ask - max_bid
    spread_dict = {
        "min_ask": "{:,.6f}".format(min_ask),
        "max_bid": "{:,.6f}".format(max_bid),
        "value": "{:,.6f}".format(value),
        "market_id": market_id,
    }
    return spread_dict


def comapre_spread_with_alert_value(
    spread_value, alert_value: str, market_id: str
) -> Dict[str, str]:
    """
    Compare the spread value with the alert value.

    **Args:**

        - spread_value (str): The spread value to be compared.
        - alert_value (str): The alert value against which the spread value is compared.
        - market_id (str): The unique identifier of the market for which the spread value is compared.

    **Returns:**

        message (Dict[str, str]): A dictionary containing the following:

            - is_greater (bool): A boolean indicating whether the spread is greater than the alert value.
            - is_less (bool): A boolean indicating whether the spread is less than the alert value.
            - message (str): A string message indicating the status of the spread alert. Possible messages include:

                - "Spread is GREATER than the alert value."
                - "Spread is LESS than the alert value."
                - "Spread is EQUAL to the alert value."

    **Raises:**

        Any exceptions raised during the data processing will be propagated.
    """

    spread_value = (float)(spread_value.replace(",", ""))
    alert_value = (float)(alert_value)
    diff = spread_value - alert_value
    diff_formatted = "{:,.8f}".format(abs(diff))
    spread_value_formatted = "{:,.8f}".format(spread_value)
    alert_value_formatted = "{:,.8f}".format(alert_value)

    if diff > 0:
        message = f"Spread for market {market_id} is GREATER than the alert value by {diff_formatted}."
    elif diff < 0:
        message = f"Spread for market {market_id} is LESS than the alert value by {diff_formatted}."
    else:
        message = f"Spread is for market {market_id} is EQUAL to the alert value."

    message += f" Spread: {spread_value_formatted}, Alert: {alert_value_formatted}"

    message_obj = {
        "is_greater": diff > 0,
        "is_less": diff < 0,
        "message": message
    }
    return message_obj
