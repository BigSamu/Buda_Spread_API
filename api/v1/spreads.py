import traceback
from typing import Any, List, Dict

from fastapi import APIRouter, HTTPException, status, Path, Body
from requests.exceptions import HTTPError

import schemas
from services import buda_api
from utils import calculate_spread

router = APIRouter()


@router.get(
    "",
    response_model=List[schemas.SpreadResponse],
    responses={
        500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
    },
)
def get_all_spreads() -> List[schemas.SpreadResponse]:
    """
    Retrieves all spreads from the Buda API.

    **Returns:**

        all_spreads (List[SpreadResponse]): A list of SpreadResponse objects in JSON format for all markets. Each object in the list includes the following fields:

            - max_bid (str): The maximum bid price for the market.
            - min_ask (str): The minimum ask price for the market.
            - spread_value (str): The calculated spread value for the market.
            - market_id (str): The unique identifier of the market.

    **Raises:**

        HTTPException:
            - 500 (Internal Server Error): For any other unexpected error.
    """
    try:
        all_spreads = []
        markets = buda_api.markets.get_all()
        for market in markets["markets"]:
            spread_dict = calculate_spread(market_id=market["id"])
            spread_obj = schemas.SpreadResponse(**spread_dict)
            all_spreads.append(spread_obj)
        return all_spreads
    except Exception as e:
        error_message = str(e)
        error_name = e.__class__.__name__
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {error_name}: {error_message}",
        )


@router.get(
    "/{market_id}",
    response_model=schemas.SpreadResponse,
    responses={
        404: {"model": schemas.ErrorResponse, "description": "Not Found"},
        500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
    },
)
async def get_spread_by_market_id(market_id: str) -> Any:
    """
    Retrieves the market spread data for a given market ID from the Buda API.

    **Path Parameters:**

        market_id (str): The unique identifier of the market for which the spread data is requested.

    **Returns:**

        spread_obj (SpreadResponse): A SpreadResponse object in JSON format for the given market. The object includes the following fields:

            - max_bid (str): The maximum bid price for the market.
            - min_ask (str): The minimum ask price for the market.
            - spread_value (str): The calculated spread value for the market.
            - market_id (str): The unique identifier of the market.

    **Raises:**

        HTTPException:
            - 404 (Not Found): If the market is not found.
            - 500 (Internal Server Error): For any other unexpected error.
            - 422 (Unprocessable Entity): If the request data is invalid or cannot be processed.

    """

    try:
        market = buda_api.markets.get_one_by_id(market_id=market_id)["market"]
        spread_dict = calculate_spread(market_id=market["id"])
        spread_obj = schemas.SpreadResponse(**spread_dict)
        return spread_obj
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
