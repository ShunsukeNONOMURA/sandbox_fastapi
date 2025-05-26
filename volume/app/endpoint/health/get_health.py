from app.endpoint.health.router import router

@router.get(
    "/health"
)
async def get_health():
    return {"message": "green"}