from pydantic import BaseModel


class SpreadResponse(BaseModel):
    max_bid: str
    min_ask: str
    value: str
    market_id: str


class SpreadAlert(BaseModel):
    value: float
