from fastapi import APIRouter

from app.api.endpoints import hotels, room_types, pricing, forecasting, analytics

api_router = APIRouter()

api_router.include_router(hotels.router, prefix="/hotels", tags=["hotels"])
api_router.include_router(room_types.router, prefix="/room-types", tags=["room-types"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["pricing"])
api_router.include_router(forecasting.router, prefix="/forecasting", tags=["forecasting"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
