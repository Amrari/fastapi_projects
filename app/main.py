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




@api_router.get("/learning_path/{path_id}", status_code=200, response_model=Learning_path)
def fetch_learning_path(*,path_id:int) -> Any:
    """
    Get learning path
    """
    result = [ learning_path for learning_path in LEARNING_PATH if ["id"] == path_id ]
    if not result:
        raise HTTPException(
            status_code=404, detail=f"path with ID {path_id} not found"
        )
    return result[0]



@api_router.get("/search", status_code=200, response_model=LPSearchResults)
def search_learning_path(
    *,
    keyword: Optional[str] = Query(None, min_length=3, examples="sql injection learning path"),               
    max_results: Optional[int] = 10
) -> dict:
                         
    if not keyword:
        return {"results": LEARNING_PATH[:max_results]}
    
    result = filter(lambda learning_path: keyword.lower() in learning_path["label"].lower(), LEARNING_PATH)
    return {"results": list(result)[:max_results]}
                         


@api_router.post("/learning_path", status_code=201, response_model=LP)
def create_learning_path(*, add_path: learning_path_create) -> dict:
    
    new_entry_id = len(LEARNING_PATH) + 1
    learning_path_entry = Learning_path(
    id= new_entry_id,
    label = add_path.label,
    URL = add_path.URL,
    source = add_path.source
    )
    LEARNING_PATH.append(learning_path_entry.dict())

    return learning_path_entry

    """
    Search learning path
    """
    # result = [ learning_path for learning_path in learning_path if search in learning_path["label"] ]
    # return {"learning_path": result}

app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
