
from fastapi import FastAPI

app = FastAPI(
    title="Smart AI Public Surveillance System",
    description="Backend API for the Public Surveillance Platform",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "message": "Smart AI Surveillance API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }
