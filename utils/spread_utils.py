from typing import Dict
from services import buda_api


def calculate_spread(market_id: str) -> Dict[str, str]:
    """
    Calculate the spread for a given market ID.

    **Args:**

        market_id (str): The unique identifier of the market for which the spread is calculated.

    **Returns:**

        Dict[str, str]: A dictionary containing the following:

            - 'min_ask': The minimum ask price for the market.
            - 'max_bid': The maximum bid price for the market.
            - 'spread_value': The calculated spread value (min_ask - max_bid) for the market.
            - 'market_id': The unique identifier of the market.

    **Raises:**

        Any exceptions raised during the API request or data processing will be propagated.
    """

    ticker = buda_api.tickers.get_one_by_market_id(market_id=market_id)["ticker"]
    min_ask = (float)(ticker["min_ask"][0])
    max_bid = (float)(ticker["max_bid"][0])
    spread_value = min_ask - max_bid
    spread_dict = {
        "min_ask": "{:,.6f}".format(min_ask),
        "max_bid": "{:,.6f}".format(max_bid),
        "spread_value": "{:,.6f}".format(spread_value),
        "market_id": market_id,
    }
    return spread_dict


def comapre_spread_with_alert_value(
    spread: Dict[str, str], alert_value: float
) -> Dict[str, str]:
    """
    Compare the spread value with the alert value.

    **Args:**

        spread (Dict[str, str]): A dictionary containing the spread data for a market, including the minimum ask price, maximum bid price, spread value, and market ID.

        alert_value (float): The alert value against which the spread value is compared.

    **Returns:**

        message (Dict[str]): A dictionary containing the following:

            - 'detail': A message indicating the status of the spread alert. Possible messages include:

                - "Spread is GREATER than the alert value."
                - "Spread is LESS than the alert value."
                - "Spread is EQUAL to the alert value."

    **Raises:**

        Any exceptions raised during the data processing will be propagated.
    """

    spread_value = (float)(spread["spread_value"])
    market_id = spread["market_id"]

    if current_spread > alert_value:
        message = "Spread is GREATER than the alert value."
    elif current_spread < alert_value:
        message = "Spread is LESS than the alert value."
    else:
        message = "Spread is EQUAL to the alert value."

    message_obj = {"detail": message}
    return message_obj
