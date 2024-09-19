from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, learning_path


api_router = APIRouter()
api_router.include_router(learning_path.api_router, prefix="/learning_path", tags=["learning_path"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])