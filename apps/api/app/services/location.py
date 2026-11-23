
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.repositories.location import LocationRepository
from apps.api.app.schemas.location import LocationCreate


class LocationService:

    @staticmethod
    async def create_location(
        db: AsyncSession,
        location_data: LocationCreate
    ):
        return await LocationRepository.create(
            db,
            location_data
        )

    @staticmethod
    async def get_all_locations(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50
    ):
        return await LocationRepository.get_all(
            db,
            skip=skip,
            limit=limit
        )

    @staticmethod
    async def get_location_by_id(
        db: AsyncSession,
        location_id: UUID
    ):
        location = await LocationRepository.get_by_id(
            db,
            location_id
        )

        if not location:
            raise ValueError("Location not found")

        return location
