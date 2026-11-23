
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.models.camera import Camera
from apps.api.app.schemas.camera import CameraCreate


class CameraRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        camera_data: CameraCreate
    ) -> Camera:

        camera = Camera(
            name=camera_data.name,
            camera_code=camera_data.camera_code,
            location_id=camera_data.location_id,
            source_url=camera_data.source_url
        )

        db.add(camera)

        try:
            await db.commit()
            await db.refresh(camera)

        except IntegrityError:
            await db.rollback()
            raise

        except Exception:
            await db.rollback()
            raise

        return camera

    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50
    ) -> list[Camera]:

        result = await db.execute(
            select(Camera)
            .order_by(Camera.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        camera_id: UUID
    ) -> Camera | None:

        result = await db.execute(
            select(Camera).where(Camera.id == camera_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_code(
        db: AsyncSession,
        camera_code: str
    ) -> Camera | None:

        result = await db.execute(
            select(Camera).where(
                Camera.camera_code == camera_code
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update_status(
        db: AsyncSession,
        camera: Camera,
        is_active: bool
    ) -> Camera:

        camera.is_active = is_active

        try:
            await db.commit()
            await db.refresh(camera)

        except Exception:
            await db.rollback()
            raise

        return camera
