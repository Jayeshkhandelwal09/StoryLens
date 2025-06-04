from fastapi import APIRouter
from app.api.endpoints import upload, stories, audio

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(upload.router, prefix="/api", tags=["upload"])
api_router.include_router(stories.router, prefix="/api", tags=["stories"])
api_router.include_router(audio.router, prefix="/api", tags=["audio"]) 