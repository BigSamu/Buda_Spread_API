from pydantic import BaseModel


class SpreadResponse(BaseModel):
    max_bid: str
    min_ask: str
    spread_value: str
    market_id: str


class SpreadAlert(BaseModel):
    alert_value: str
    market_id: str
