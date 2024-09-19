from http.client import HTTPException
from pathlib import Path
import time
from typing import Any, Optional
from fastapi import FastAPI, APIRouter, Query , Request
import uvicorn
from app.schemas.learning_path import LPSearchResults ,LP , learning_path_create,Learning_path
from app.learning_path_data import LEARNING_PATH
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.api.api_v1.api import api_router
# Create FastAPI instance

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title="fashion API", openapi_url="/openapi.json")

router = APIRouter()

@router.get("/", status_code=200)
def root(request: Request) -> dict:
    """
    Root GET
    """ 
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "learning_paths": LEARNING_PATH}
    )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(router)
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    # Use this for debugging purposes only
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
