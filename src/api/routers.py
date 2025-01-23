from fastapi import APIRouter

from api.endpoints import product_router, subscribe_router, user_router

main_router = APIRouter()
main_router.include_router(
    product_router, prefix="/products", tags=["Product"]
)
main_router.include_router(
    subscribe_router, prefix="/subscribe", tags=["Subscribe"]
)
main_router.include_router(user_router)
