from typing import Any, List, Dict

from fastapi import APIRouter, HTTPException, status


from api import schemas
from services import buda_api

router = APIRouter()

@router.get("/spreads", response_model=List[schemas.Spread])
async def get_spreads():
    """
    Retrieves all spreads from the BUDA API.

    Returns:
        Dict[str, Any]: A dictionary containing the JSON response with all spreads.
    """
    spreads = buda_api.get_all_markets()
    return spreads
