from fastapi import FastAPI
from apps.api.app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for the Public Surveillance Platform",
    version=settings.APP_VERSION
)


@app.get("/")
async def root():
    return {
        "message": "Smart AI Surveillance API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }