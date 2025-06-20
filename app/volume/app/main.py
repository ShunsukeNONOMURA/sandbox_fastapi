from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi_mcp import FastApiMCP

from app.endpoint.router import main_router

app = FastAPI()
app.include_router(main_router)

mcp = FastApiMCP(
    app,
    name="My API MCP",
    description="My API description",
    # base_url="http://localhost:8000",
)

# Mount the MCP server directly to your FastAPI app
mcp.mount()

# mount gradio ui
from gradio import mount_gradio_app
from app.ui.ui import interface
app = mount_gradio_app(app, interface, path="/gradio")