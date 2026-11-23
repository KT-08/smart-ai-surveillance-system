
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.models.location import Location
from apps.api.app.schemas.location import LocationCreate


class LocationRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        location_data: LocationCreate
    ) -> Location:

        location = Location(
            name=location_data.name,
            latitude=location_data.latitude,
            longitude=location_data.longitude
        )

        db.add(location)

        try:
            await db.commit()
            await db.refresh(location)

        except Exception:
            await db.rollback()
            raise

        return location

    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50
    ) -> list[Location]:

        result = await db.execute(
            select(Location)
            .order_by(Location.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        location_id: UUID
    ) -> Location | None:

        result = await db.execute(
            select(Location).where(Location.id == location_id)
        )

        return result.scalar_one_or_none()
