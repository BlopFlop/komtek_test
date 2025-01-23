"""API endpoints package."""

from api.endpoints.product import router as product_router
from api.endpoints.subscribe import router as subscribe_router
from api.endpoints.user import router as user_router

__all__ = ["product_router", "subscribe_router", "user_router"]
