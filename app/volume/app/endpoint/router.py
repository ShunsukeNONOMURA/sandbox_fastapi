from fastapi import APIRouter

from app.endpoint import (
    health,
    user,
)

# メインルータ作成
main_router = APIRouter()

main_router.include_router(health.router, tags=["Health"])
main_router.include_router(user.router, tags=["User"])