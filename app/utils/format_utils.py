from typing import Dict


def format_current_spread(current_spread: Dict[str, str]) -> Dict[str, str]:
    """
    Format the spread dictionary to include formatted values.

    **Args:**

        - spread_dict (Dict[str, Any]): A dictionary containing the spread details.

    **Returns:**

        current_spread_formatted (Dict[str, str]): A dictionary containing the spread details with formatted values. The formatted values include the following fields:

            - min_ask (str): The minimum ask price for the market with 6 decimal places and comma separated thousands.
            - max_bid (str): The maximum bid price for the market with 6 decimal places and comma separated thousands.
            - value (str): The calculated spread value (min_ask - max_bid) for the market with 6 decimal places and comma separated thousands.
            - market_id (str): The unique identifier of the market.

    **Raises:**

        Any exceptions raised during the data processing will be propagated.
    """
    try:
        current_spread_formatted = {
            "min_ask": "{:,.6f}".format(current_spread["min_ask"]),
            "max_bid": "{:,.6f}".format(current_spread["max_bid"]),
            "value": "{:,.6f}".format(current_spread["value"]),
            "market_id": current_spread["market_id"],
        }

        return current_spread_formatted

    except ValueError as e:
        raise ValueError(
            f"Error formatting spread for market {current_spread['market_id']}: {str(e)}"
        )
    except KeyError as e:
        raise KeyError(
            f"Error formatting spread for market {current_spread['market_id']}: {str(e)}"
        )
