import traceback
from typing import Any, List, Dict

from fastapi import APIRouter, HTTPException, status, Path, Body
from requests.exceptions import HTTPError

from app import schemas
from app.services import buda_api
from app.utils import calculate_spread, comapre_spread_with_alert_value

router = APIRouter()
spread_alert = {"value": None}

@router.get(
    "",
    response_model=Dict[str, schemas.AlertMessage],
    responses={
        404: {"model": schemas.ErrorResponse, "description": "Not Found"},
        500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
    },
)
async def compare_alert_with_all_markets() -> Dict[str, schemas.AlertMessage]:
    """
    Get the spread alert status for all markets.

    **Path Parameters:**

        market_id (str): The unique identifier of the market for which the spread data is requested.

    **Returns:**

        message_alerts (Dict[str, AlertMessage]): A dictionary containing the status of the spread alert for all markets. The dictionary includes the market ID as the key and an AlertMessage object as the value. The AlertMessage object includes the following fields:

            - is_greater (bool): A boolean indicating whether the spread is greater than the alert value.
            - is_less (bool): A boolean indicating whether the spread is less than the alert value.
            - message (str): A string message indicating the status of the spread alert. Possible messages include:

                - "Spread is GREATER than the alert value."
                - "Spread is LESS than the alert value."
                - "Spread is EQUAL to the alert value."

    **Raises:**

        HTTPException:
            - 404 (Not Found): If the market is not found.
            - 500 (Internal Server Error): For any other unexpected error.
    """

    if not spread_alert["value"]:
        raise HTTPException(
            status_code=404, detail="Spread Alert not set yet. Please one first."
        )

    try:
        markets = buda_api.markets.get_all()
        alert_value = spread_alert["value"]
        message_alerts = {}
        for market in markets["markets"]:
            current_spread = calculate_spread(market_id=market["id"])
            spread_value = current_spread["value"]
            message = comapre_spread_with_alert_value(spread_value, alert_value, market["id"])
            message_alerts[market["id"]] = message
        return message_alerts

    except HTTPError as http_err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(f"Market with id '{market_id}' not found"),
        )
    except Exception as e:
        error_message = str(e)
        error_name = e.__class__.__name__
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {error_name}: {error_message}",
        )

@router.get(
    "/{market_id}",
    response_model=schemas.AlertMessage,
    responses={
        404: {"model": schemas.ErrorResponse, "description": "Not Found"},
        500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
        422: {"model": schemas.ErrorResponse, "description": "Unprocessable Entity"},
    },
)
async def compare_alert_with_one_market(market_id: str) -> schemas.Message:
    """
    Get the spread alert status for a given market.

    **Path Parameters:**

        market_id (str): The unique identifier of the market for which the spread data is requested.

    **Returns:**

        message_alert (AlertMessage): An AlertMessage object in JSON format indicating the status of the spread alert for the given market. The object includes the following fields:

            - is_greater (bool): A boolean indicating whether the spread is greater than the alert value.
            - is_less (bool): A boolean indicating whether the spread is less than the alert value.
            - message (str): A string message indicating the status of the spread alert. Possible messages include:

                - "Spread is GREATER than the alert value."
                - "Spread is LESS than the alert value."
                - "Spread is EQUAL to the alert value."

    **Raises:**

        HTTPException:
            - 404 (Not Found): If the market is not found.
            - 500 (Internal Server Error): For any other unexpected error.
            - 422 (Unprocessable Entity): If the request data is invalid or cannot be processed.
    """

    if not spread_alert["value"]:
        raise HTTPException(
            status_code=404, detail="Spread Alert not set yet. Please one first."
        )

    try:
        market = buda_api.markets.get_one_by_id(market_id=market_id)
        alert_value = spread_alert["value"]
        current_spread = calculate_spread(market_id=market_id)
        spread_value = current_spread["value"]
        message_alert = comapre_spread_with_alert_value(spread_value, alert_value, market_id)
        return message_alert

    except HTTPError as http_err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(f"Market with id '{market_id}' not found"),
        )
    except Exception as e:
        error_message = str(e)
        error_name = e.__class__.__name__
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {error_name}: {error_message}",
        )


@router.post(
    "",
    response_model=schemas.Message,
    responses={
        404: {"model": schemas.ErrorResponse, "description": "Not Found"},
        500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
        422: {"model": schemas.ErrorResponse, "description": "Unprocessable Entity"},
    },
)
async def set_spread_alert(alert: schemas.SpreadAlert) -> schemas.Message:
    """
    Sets an spread alert for a given market.

    **Request Body:**

        alert (SpreadAlert): A SpreadAlert object in JSON format. The object requires the following fields:

            - alert_value (str): The value of the spread alert.

    **Returns:**

        message (Message): A message object in JSON format with information about the alert set operation. The object includes the following fields:
            - message (str): A message indicating the alert was set correctly.

    **Raises:**

        HTTPException:
            - 404 (Not Found): If the market is not found.
            - 500 (Internal Server Error): For any other unexpected error.
            - 422 (Unprocessable Entity): If the request data is invalid or cannot be processed.
    """
    try:
        spread_alert["value"]=alert.value
        message = {"message": "Alert set successfully"}
        return message
    except Exception as e:
        error_message = str(e)
        error_name = e.__class__.__name__
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {error_name}: {error_message}",
        )
