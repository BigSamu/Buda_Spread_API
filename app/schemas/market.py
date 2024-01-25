from pydantic import BaseModel
from typing import Optional, List


class MarketResponse(BaseModel):
    id: str
    name: Optional[str] = None
    base_currency: Optional[str] = None
    quote_currency: Optional[str] = None
    minimum_order_amount: Optional[List[str]] = None
    disabled: Optional[bool] = None
    illiquid: Optional[bool] = None
    rpo_disabled: Optional[bool] = None
    taker_fee: Optional[float] = None
    maker_fee: Optional[float] = None
    max_orders_per_minute: Optional[int] = None
    maker_discount_percentage: Optional[str] = None
    taker_discount_percentage: Optional[str] = None
