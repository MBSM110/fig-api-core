from fastapi import APIRouter, Depends
from app.api.v1.endpoints import coins
from app.api.deps import get_internal_api_key

api_router = APIRouter()
api_router.include_router(
    coins.router,
    prefix="/coins",
    tags=["coins"],
    dependencies=[Depends(get_internal_api_key)]
    )