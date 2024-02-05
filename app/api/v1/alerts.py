import traceback
from typing import Any, List, Dict

from fastapi import APIRouter, HTTPException, status, Path, Body
from pydantic import ValidationError
from requests.exceptions import HTTPError

from app import schemas
from app.services import buda_api
from app.utils import calculate_spread, compare_spread_with_alert_value

router = APIRouter()
spread_alert = {"value": None}


@router.get(
    "",
    response_model=Dict[str, schemas.AlertResponse],
    responses={
        404: {"model": schemas.ErrorResponse, "description": "Not Found"},
        500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
    },
)
async def compare_alert_with_all_markets() -> Dict[str, schemas.AlertResponse]:
    """
    Compare the spread alert for all markets from the Buda API.

    **Path Parameters:**

        market_id (str): The unique identifier of the market for which the spread data is requested.

    **Returns:**

        alerts (Dict[str, AlertResponse]): A dictionary containing the status of the spread alert for all markets. The dictionary includes the market ID as the key and an AlertResponse object as the value. The AlertResponse object includes the following fields:

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

        HTTPException:

            - 404 (Not Found): If the market is not found.
            - 500 (Internal Server Error): For any other unexpected error.
    """

    if not spread_alert["value"]:
        raise HTTPException(
            status_code=404, detail="Spread Alert not set yet. Please set one first."
        )

    try:
        markets = buda_api.markets.get_all()
        alert_value = spread_alert["value"]
        alerts = {}
        for market in markets["markets"]:
            ticker = schemas.TickerResponse(
                **buda_api.tickers.get_one_by_market_id(market_id=market["id"])[
                    "ticker"
                ]
            ).model_dump()
            current_spread = calculate_spread(ticker)
            alert = compare_spread_with_alert_value(
                spread_value=current_spread["value"],
                alert_value=spread_alert["value"],
                market_id=market["id"],
            )
            alerts[market["id"]] = alert
        return alerts

    except ValidationError as e:
        error_details = json.loads(e.json())
        raise HTTPException(status_code=422, detail={"detail": error_details})

    except Exception as err:
        error_message = str(err)
        error_name = err.__class__.__name__
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {error_name}: {error_message}",
        )


@router.get(
    "/{market_id}",
    response_model=schemas.AlertResponse,
    responses={
        404: {"model": schemas.ErrorResponse, "description": "Not Found"},
        500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
    },
)
async def compare_alert_with_one_market(market_id: str) -> schemas.AlertResponse:
    """
    Compare the spread alert for a given market from the Buda API.

    **Path Parameters:**

        market_id (str): The unique identifier of the market for which the spread data is requested.

    **Returns:**

        alert (AlertResponse): An AlertResponse object in JSON format indicating the status of the spread alert for the given market. The object includes the following fields:

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

        HTTPException:

            - 404 (Not Found): If the market is not found.
            - 422 (Unprocessable Entity): If the request data is invalid or cannot be processed.
            - 500 (Internal Server Error): For any other unexpected error.
    """

    if not spread_alert["value"]:
        raise HTTPException(
            status_code=404, detail="Spread Alert not set yet. Please set one first."
        )

    try:
        ticker = buda_api.tickers.get_one_by_market_id(market_id=market_id)["ticker"]
        current_spread = calculate_spread(ticker)
        alert = compare_spread_with_alert_value(
            spread_value=current_spread["value"],
            alert_value=spread_alert["value"],
            market_id=market_id,
        )
        return alert

    except ValidationError as e:
        error_details = json.loads(e.json())
        raise HTTPException(status_code=422, detail={"detail": error_details})

    except Exception as err:
        if err.response is not None and err.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(f"Market with id '{market_id}' not found"),
            )

        error_message = str(err)
        error_name = err.__class__.__name__
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
    },
)
async def set_spread_alert(alert: schemas.SpreadAlert) -> schemas.Message:
    """
    Sets an spread alert for a given market from the Buda API.

    **Request Body:**

        alert (SpreadAlert): A SpreadAlert object in JSON format. The object requires the following fields:

            - alert_value (float): The value of the spread alert.

    **Returns:**

        message (Message): A message object in JSON format with information about the alert set operation. The object includes the following fields:

            - message (str): A message indicating the alert was set correctly.

    **Raises:**

        HTTPException:

            - 422 (Unprocessable Entity): If the request data is invalid or cannot be processed.
            - 500 (Internal Server Error): For any other unexpected error.
    """
    try:
        spread_alert["value"] = alert.value
        alert_value_formatted = "{:,.2f}".format(alert.value)
        message = {
            "message": f"Alert set successfully. Alert value: {alert_value_formatted}"
        }
        return message

    except ValidationError as e:
        error_details = json.loads(e.json())
        raise HTTPException(status_code=422, detail={"detail": error_details})

    except Exception as err:
        if isinstance(err, HTTPError) and err.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(f"Market with id '{market_id}' not found"),
            )

        error_message = str(err)
        error_name = err.__class__.__name__
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {error_name}: {error_message}",
        )
