from pydantic import BaseModel


class AlertResponse(BaseModel):
    market_id: str
    spread_value: str
    alert_value: str
    is_greater: bool
    is_less: bool
    message: str
