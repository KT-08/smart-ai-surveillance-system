
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.db.session import get_db
from apps.api.app.schemas.camera import (
    CameraCreate,
    CameraResponse,
    CameraStatusUpdate
)
from apps.api.app.services.camera import CameraService
from apps.api.app.core.dependencies import require_role
from apps.api.app.models.user import User


router = APIRouter(
    prefix="/cameras",
    tags=["Cameras"]
)


# 1. REGISTER CAMERA

@router.post(
    "/",
    response_model=CameraResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_camera(
    camera_data: CameraCreate,
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    try:
        return await CameraService.create_camera(
            session,
            camera_data
        )

    except ValueError as error:
        message = str(error)

        if message == "Location not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message
            )

        if message == "Camera code already exists":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message
            )

        raise

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Camera registration conflicts with an existing database record"
        )


# 2. GET ALL CAMERAS

@router.get(
    "/",
    response_model=list[CameraResponse]
)
async def list_cameras(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    return await CameraService.get_all_cameras(
        session,
        skip=skip,
        limit=limit
    )


# 3. GET CAMERA BY ID

@router.get(
    "/{camera_id}",
    response_model=CameraResponse
)
async def get_camera_details(
    camera_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    try:
        return await CameraService.get_camera_by_id(
            session,
            camera_id
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )


# 4. ACTIVATE / DEACTIVATE CAMERA

@router.patch(
    "/{camera_id}/status",
    response_model=CameraResponse
)
async def update_camera_status(
    camera_id: UUID,
    status_data: CameraStatusUpdate,
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    try:
        return await CameraService.update_camera_status(
            session,
            camera_id,
            status_data.is_active
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )