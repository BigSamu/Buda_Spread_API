import traceback
from typing import Any, List, Dict

from fastapi import APIRouter, HTTPException, status, Path, Body
from requests.exceptions import HTTPError

import schemas
from services import buda_api
from utils import calculate_spread, comapre_spread_with_alert_value

router = APIRouter()
spread_alert_in_memory: int = None


@router.get(
    "",
    response_model=schemas.Message,
    responses={
        404: {"model": schemas.ErrorResponse, "description": "Not Found"},
        500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
        422: {"model": schemas.ErrorResponse, "description": "Unprocessable Entity"},
    },
)
async def get_alert_for_market(market_id: str) -> schemas.Message:
    """
    Get the spread alert status for a given market.

    **Path Parameters:**

        market_id (str): The unique identifier of the market for which the spread data is requested.

    **Returns:**

        message (Message): A message object in JSON format indicating the status of the spread alert for the given market.

    **Raises:**

        HTTPException:
            - 404 (Not Found): If the market is not found.
            - 500 (Internal Server Error): For any other unexpected error.
            - 422 (Unprocessable Entity): If the request data is invalid or cannot be processed.
    """

    if not spread_alert_in_memory:
        raise HTTPException(
            status_code=404, detail="Spread Alert not set yet. Please one first."
        )

    try:
        market = buda_api.markets.get_one_by_id(market_id=market_id)
        market_id = market["market"]["id"]
        alert_value = float(spread_alerts_in_memory[market_id])

        current_spread = calculate_spread(market_id=market_id)
        message = comapre_spread_with_alert_value(current_spread, alert_value)

        return {"detail": message}

    except HTTPError as http_err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(f"Market with id '{market_id}' not found"),
        )
    except Exception as e:
        error_message = str(e)
        error_name = e.__class__.__name__
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
async def set_alert_for_market(alert: schemas.SpreadAlert) -> schemas.Message:
    """
    Sets an spread alert for a given market.

    **Request Body:**

        alert (SpreadAlert): A SpreadAlert object in JSON format to be set for the given market ID. The object requires the following fields:
            - alert_value (str): The value of the spread alert.
            - market_id (str): The unique identifier of the market for which the alert is being set.

    **Returns:**

        message (Message): A message object in JSON format with information about the alert set operation. The object includes the following fields:
            - detail (str): A message indicating the alert was set correctly.

    **Raises:**

        HTTPException:
            - 404 (Not Found): If the market is not found.
            - 500 (Internal Server Error): For any other unexpected error.
            - 422 (Unprocessable Entity): If the request data is invalid or cannot be processed.
    """
    try:
        market = buda_api.markets.get_one_by_id(market_id=alert.market_id)
        market_id = market["market"]["id"]
        spread_alerts_in_memory[market_id] = alert.alert_value
        return {"message": "Alert set successfully"}
    except HTTPError as http_err:
        if http_err.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(f"Market with id '{alert.market_id}' not found"),
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(f"Market with id '{alert.market_id}' not found"),
        )
    except Exception as e:
        error_message = str(e)
        error_name = e.__class__.__name__
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {error_name}: {error_message}",
        )
