from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional
from app import crud
from app.api import deps
from app.learning_path_data import LEARNING_PATH
from app.schemas.learning_path import LPSearchResults ,LP , learning_path_create,Learning_path


api_router = APIRouter()

@api_router.get("/{path_id}", status_code=200, response_model=Learning_path)
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