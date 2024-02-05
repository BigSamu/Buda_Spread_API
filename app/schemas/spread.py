from pydantic import BaseModel


class SpreadResponse(BaseModel):
    market_id: str
    value: str
    max_bid: str
    min_ask: str


class SpreadAlert(BaseModel):
    value: float
