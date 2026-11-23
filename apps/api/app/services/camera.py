
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.repositories.camera import CameraRepository
from apps.api.app.repositories.location import LocationRepository
from apps.api.app.schemas.camera import CameraCreate


class CameraService:

    @staticmethod
    async def create_camera(
        db: AsyncSession,
        camera_data: CameraCreate
    ):
        # Check whether the selected location exists
        location = await LocationRepository.get_by_id(
            db,
            camera_data.location_id
        )

        if not location:
            raise ValueError("Location not found")

        # Check whether the camera code already exists
        existing_camera = await CameraRepository.get_by_code(
            db,
            camera_data.camera_code
        )

        if existing_camera:
            raise ValueError("Camera code already exists")

        # Create the camera
        return await CameraRepository.create(db, camera_data)

    @staticmethod
    async def get_all_cameras(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50
    ):
        return await CameraRepository.get_all(
            db,
            skip=skip,
            limit=limit
        )

    @staticmethod
    async def get_camera_by_id(
        db: AsyncSession,
        camera_id: UUID
    ):
        camera = await CameraRepository.get_by_id(
            db,
            camera_id
        )

        if not camera:
            raise ValueError("Camera not found")

        return camera

    @staticmethod
    async def update_camera_status(
        db: AsyncSession,
        camera_id: UUID,
        is_active: bool
    ):
        camera = await CameraRepository.get_by_id(
            db,
            camera_id
        )

        if not camera:
            raise ValueError("Camera not found")

        return await CameraRepository.update_status(
            db,
            camera,
            is_active
        )
