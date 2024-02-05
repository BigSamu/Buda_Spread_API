from pydantic import BaseModel, field_validator
from typing import List, Optional


class TickerResponse(BaseModel):
    market_id: str
    last_price: Optional[List[str]] = None
    min_ask: List[str]
    max_bid: List[str]
    volume: Optional[List[str]] = None
    price_variation_24h: Optional[str] = None
    price_variation_7d: Optional[str] = None

    @field_validator("min_ask", "max_bid")
    def check_list_structure(cls, v):
        if not isinstance(v, list) or len(v) != 2:
            raise ValueError("must be a list of 2 elements")
        if not v[0].replace(".", "").isnumeric():
            raise ValueError("The first element must be able to cast to a float")
        return v
