from app.endpoint.user.router import router

@router.get(
    "/users/{user_id}"
)
async def get_user(
    user_id: str,
):
    return {"user_id": user_id}