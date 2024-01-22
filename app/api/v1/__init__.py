from fastapi import APIRouter
from app.api.v1 import spreads, alerts

api_router = APIRouter()
api_router.include_router(spreads.router, prefix="/spreads", tags=["spreads"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
