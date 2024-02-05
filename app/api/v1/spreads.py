import traceback
from typing import Any, List, Dict
import json

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response, JSONResponse
from pydantic import ValidationError
from requests.exceptions import HTTPError

from app import schemas
from app.services import buda_api
from app.utils import calculate_spread, format_current_spread

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

            - market_id (str): The unique identifier of the market.
            - value (str): The calculated spread value for the market.
            - max_bid (str): The maximum bid price for the market.
            - min_ask (str): The minimum ask price for the market.

    **Raises:**

        HTTPException:

            - 422 (Unprocessable Entity): If the request data is invalid or cannot be processed.
            - 500 (Internal Server Error): For any other unexpected error.
    """
    try:
        all_spreads = []
        markets = buda_api.markets.get_all()
        for market in markets["markets"]:
            market = schemas.MarketResponse(**market).model_dump()
            ticker = schemas.TickerResponse(
                **buda_api.tickers.get_one_by_market_id(market_id=market["id"])[
                    "ticker"
                ]
            ).model_dump()
            current_spread = calculate_spread(ticker=ticker)
            current_spread_formatted = format_current_spread(current_spread)
            all_spreads.append(schemas.SpreadResponse(**current_spread_formatted))
        return all_spreads

    except ValidationError as e:
        error_details = json.loads(e.json())
        raise HTTPException(status_code=422, detail={"detail": error_details})

    except Exception as err:

        if isinstance(err, HTTPError) and err.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(f"Market not found"),
            )

        error_message = str(err)
        error_name = err.__class__.__name__
        print(traceback.format_exc())
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
def get_spread_by_market_id(market_id: str) -> Any:
    """
    Retrieves the market spread data for a given market ID from the Buda API.

    **Path Parameters:**

        market_id (str): The unique identifier of the market for which the spread data is requested.

    **Returns:**

        spread_obj (SpreadResponse): A SpreadResponse object in JSON format for the given market. The object includes the following fields:

            - market_id (str): The unique identifier of the market.
            - spread_value (str): The calculated spread value for the market.
            - max_bid (str): The maximum bid price for the market.
            - min_ask (str): The minimum ask price for the market.

    **Raises:**

        HTTPException:

            - 404 (Not Found): If the market is not found.
            - 422 (Unprocessable Entity): If the request data is invalid or cannot be processed.
            - 500 (Internal Server Error): For any other unexpected error.

    """

    try:
        ticker = schemas.TickerResponse(
            **buda_api.tickers.get_one_by_market_id(market_id=market_id)["ticker"]
        ).model_dump()
        current_spread = calculate_spread(ticker=ticker)
        current_spread_formatted = format_current_spread(current_spread)
        return schemas.SpreadResponse(**current_spread_formatted)

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
