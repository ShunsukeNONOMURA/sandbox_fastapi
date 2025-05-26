from fastapi import FastAPI

from app.endpoint.router import main_router

app = FastAPI()
app.include_router(main_router)
