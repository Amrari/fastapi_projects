from http.client import HTTPException
from pathlib import Path
from typing import Any, Optional
from fastapi import FastAPI, APIRouter, Query , Request
import uvicorn
from app.schemas.learning_path import LPSearchResults ,LP , learning_path_create,Learning_path
from app.learning_path_data import LEARNING_PATH
from fastapi.templating import Jinja2Templates


# Create FastAPI instance

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title="fashion API", openapi_url="/openapi.json")

api_router = APIRouter()

@api_router.get("/", status_code=200)
def root(request: Request) -> dict:
    """
    Root GET
    """ 
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "learning_paths": LEARNING_PATH}
    )

app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
