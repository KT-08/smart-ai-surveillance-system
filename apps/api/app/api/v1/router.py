
from fastapi import APIRouter

from apps.api.app.api.v1.endpoints import auth, users,locations,cameras


api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(locations.router)
api_router.include_router(cameras.router)
