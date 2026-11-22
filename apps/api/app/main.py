
from fastapi import FastAPI

from apps.api.app.core.config import settings
from apps.api.app.api.v1.router import api_router


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for the Public Surveillance Platform",
    version=settings.APP_VERSION
)


# Register API routes
app.include_router(
    api_router,
    prefix="/api/v1"
)


@app.get("/")
async def root():
    return {
        "message": "Smart AI Public Surveillance System API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }
