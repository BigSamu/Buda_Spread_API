from pydantic import BaseModel


class Message(BaseModel):
    message: str


class AlertMessage(BaseModel):
    is_greater: bool
    is_less: bool
    message: str
