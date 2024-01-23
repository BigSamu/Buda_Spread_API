from typing import Dict

def format_spread_dict(spread_dict: Dict[str, str]) -> Dict[str, str]:
    """
    Format the spread dictionary to include formatted values.

    **Args:**

        - spread_dict (Dict[str, Any]): A dictionary containing the spread details.

    **Returns:**

        formatted_spread_dict (Dict[str, str]): A dictionary containing the spread details with formatted values. The formatted values include the following fields:

            - min_ask (str): The minimum ask price for the market with 6 decimal places and comma separated thousands.
            - max_bid (str): The maximum bid price for the market with 6 decimal places and comma separated thousands.
            - value (str): The calculated spread value (min_ask - max_bid) for the market with 6 decimal places and comma separated thousands.
            - market_id (str): The unique identifier of the market.

    **Raises:**

        Any exceptions raised during the data processing will be propagated.
    """
    try:
        formatted_spread_dict = {
            "min_ask": "{:,.6f}".format(spread_dict["min_ask"]),
            "max_bid": "{:,.6f}".format(spread_dict["max_bid"]),
            "value": "{:,.6f}".format(spread_dict["value"]),
            "market_id": spread_dict["market_id"],
        }

    except ValueError as e:
        raise ValueError(f"Error formatting spread for market {spread_dict['market_id']}: {str(e)}")
    except KeyError as e:
        raise KeyError(f"Error formatting spread for market {spread_dict['market_id']}: {str(e)}")
    return formatted_spread_dict
