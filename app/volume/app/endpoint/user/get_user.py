from app.endpoint.user.router import router
from app.infrastructure.database.db import get_session

from fastapi import Depends
from sqlmodel import Session

@router.get(
    "/users/{user_id}"
)
async def get_user(
    user_id: str,
    session: Session = Depends(get_session),
):
    from app.domain.repository import UserRepository
    user_repository = UserRepository(session)
    user = user_repository.find_by_id(user_id)

    return user
