from pydantic import BaseModel


class Spread(BaseModel):
    max_bid: float
    min_ask: float
    spread: float
    market_id: str
