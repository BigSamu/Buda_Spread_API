from fastapi import APIRouter
from api.v1 import spreads

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/spreads", tags=["spreads"])
