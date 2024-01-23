from typing import Dict
from app.services import buda_api

def calculate_spread(min_ask: str, max_bid: str, market_id: str) -> Dict[str, str]:
    """
    Calculate the spread for a given market ID.

    **Args:**

        - min_ask (str): The minimum ask price for the market.
        - max_bid (str): The maximum bid price for the market.
        - market_id (str): The unique identifier of the market for which the spread is calculated.

    **Returns:**

        Dict[str, str]: A dictionary containing the following:

            - 'min_ask': The minimum ask price for the market.
            - 'max_bid': The maximum bid price for the market.
            - 'value': The calculated spread value (min_ask - max_bid) for the market.
            - 'market_id': The unique identifier of the market.

    **Raises:**

        A ValueError will be raised if the spread value or alert value cannot be converted to a float.
    """

    try:
        min_ask_num = (float)(min_ask)
        max_bid_num = (float)(max_bid)
        spread_dict = {
            "min_ask": min_ask_num,
            "max_bid": max_bid_num,
            "value": min_ask_num - max_bid_num,
            "market_id": market_id,
        }
        return spread_dict
    except ValueError as e:
        raise ValueError(f"Error calculating spread for market {market_id}: {str(e)}")


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

        message (Dict[str, str]): A dictionary containing the following:

            - is_greater (bool): A boolean indicating whether the spread is greater than the alert value.
            - is_less (bool): A boolean indicating whether the spread is less than the alert value.
            - message (str): A string message indicating the status of the spread alert. Possible messages include:

                - "Spread is GREATER than the alert value."
                - "Spread is LESS than the alert value."
                - "Spread is EQUAL to the alert value."

    **Raises:**

        A ValueError will be raised if the spread value or alert value cannot be converted to a float.
    """
    try:
        spread_value = (float)(spread_value)
        alert_value = (float)(alert_value)
        diff = spread_value - alert_value
        alert_dict = {
            "spread_value": spread_value,
            "alert_value": alert_value,
            "diff": diff,
        }
        alert_dict_formatted = {
            "spread_value": "{:,.2f}".format(alert_dict["spread_value"]),
            "alert_value": "{:,.2f}".format(alert_dict["alert_value"]),
            "diff": "{:,.2f}".format(abs(alert_dict["diff"])),
        }

        if diff > 0:
            message = f"Spread for market {market_id} is GREATER than the alert value by {alert_dict_formatted['diff']}."
        elif diff < 0:
            message = f"Spread for market {market_id} is LESS than the alert value by {alert_dict_formatted['diff']}."
        else:
            message = f"Spread is for market {market_id} is EQUAL to the alert value."

        message += f" Spread Value: {alert_dict_formatted['spread_value']}, Alert Value: {alert_dict_formatted['alert_value']}"

        message_obj = {
            "is_greater": diff > 0,
            "is_less": diff < 0,
            "message": message
        }
        return message_obj
    except ValueError as e:
        raise ValueError(f"Error calculating spread for market {market_id}: {str(e)}")
