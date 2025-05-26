from fastapi import APIRouter

from app.endpoint import (
    health,
)

# メインルータ作成
main_router = APIRouter()

main_router.include_router(health.router, tags=["Health"])