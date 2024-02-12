from typing import Optional
from pydantic import BaseModel


class AlertCreate(BaseModel):
    value: float

class AlertCreate(BaseModel):
    value: Optional[float]

class AlertResponse(BaseModel):
    market_id: str
    spread_value: str
    alert_value: str
    is_greater: bool
    is_less: bool
    message: str
