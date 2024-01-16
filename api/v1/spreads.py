from typing import Any, List, Dict

from fastapi import APIRouter, HTTPException, status
from requests.exceptions import HTTPError

import schemas
from services import buda_api

router = APIRouter()


@router.get("", response_model=List[schemas.SpreadResponse],responses={
        500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
    },)
async def get_all_spreads() -> List[schemas.SpreadResponse]:
    """
    Retrieves all spreads from the BUDA API.

    Returns:
        List[schemas.SpreadResponse]: A list of spread data entry for all markets.

    Raises:
        HTTPException: A 500 error for any other unexpected error.
    """
    try:
        all_spreads = []
        markets = buda_api.markets.get_all()
        for market in markets["markets"]:
            ticker = buda_api.tickers.get_one_by_market_id(market_id = market["id"])
            min_ask = (float) (ticker["ticker"]["min_ask"][0])
            max_bid = (float) (ticker["ticker"]["max_bid"][0])
            spread_dict = {
                "min_ask": min_ask,
                "max_bid": max_bid,
                "spread": min_ask-max_bid,
                "market_id": market["id"]
            }
            spread_obj = schemas.SpreadResponse(**spread_dict)
            all_spreads.append(spread_obj)
        return all_spreads
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )


@router.get(
    "/",
    response_model=schemas.SpreadResponse,
    responses={
        404: {"model": schemas.ErrorResponse, "description": "Spread for Market Not Found"},
        500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
    },
)
async def get_spread_by_market_id(market_id: str) -> Any:
    """
    Retrieves the market spread data for a given market ID from the Buda API.

    Args:
        market_id (str): The unique identifier of the market for which the spread data is requested.

    Returns:
        schemas.SpreadResponse: A spread data entry for the given market.

    Raises:
        HTTPException: A 404 error if the market is not found, or a 500 error for any other unexpected error.
    """
    try:
        ticker = buda_api.tickers.get_one_by_market_id(market_id = market_id)
        min_ask = (float) (ticker["ticker"]["min_ask"][0])
        max_bid = (float) (ticker["ticker"]["max_bid"][0])
        spread_dict = {
            "min_ask": min_ask,
            "max_bid": max_bid,
            "spread": min_ask-max_bid,
            "market_id": market_id
        }
        spread_obj = schemas.SpreadResponse(**spread_dict)
        return spread_obj
    except HTTPError as http_err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(http_err)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )
