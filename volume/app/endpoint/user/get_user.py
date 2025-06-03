from app.endpoint.user.router import router

@router.get(
    "/users/{user_id}"
)
async def get_user(
    user_id: str,
):
    return {"message": user_id}