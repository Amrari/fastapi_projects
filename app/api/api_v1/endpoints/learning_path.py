import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional
from app import crud
from app.api import deps
from app.learning_path_data import LEARNING_PATH
from app.schemas.learning_path import LPSearchResults ,LP , learning_path_create,Learning_path
import httpx

api_router = APIRouter()
LEARNING_PATH_SUBREDDITS = ["learning_path", "easylevels", "Toplevels"]

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


async def get_reddit_top_async(subreddit: str) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
            headers={"User-agent": "learning_path bot 0.1"},
        )

    subreddit_learning_path = response.json()
    subreddit_data = []
    for entry in subreddit_learning_path["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    return subreddit_data


def get_reddit_top(subreddit: str) -> list:
    response = httpx.get(
        f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
        headers={"User-agent": "learning_path bot 0.1"},
    )
    subreddit_learning_path = response.json()
    subreddit_data = []
    for entry in subreddit_learning_path["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    return subreddit_data


@api_router.get("/ideas/async")
async def fetch_ideas_async() -> dict:
    results = await asyncio.gather(
        *[get_reddit_top_async(subreddit=subreddit) for subreddit in LEARNING_PATH_SUBREDDITS]
    )
    return dict(zip(LEARNING_PATH_SUBREDDITS, results))


@api_router.get("/ideas/")
def fetch_ideas() -> dict:
    return {key: get_reddit_top(subreddit=key) for key in LEARNING_PATH_SUBREDDITS}
