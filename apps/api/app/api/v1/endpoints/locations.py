
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.db.session import get_db
from apps.api.app.schemas.location import (
    LocationCreate,
    LocationResponse
)
from apps.api.app.services.location import LocationService
from apps.api.app.core.dependencies import require_role
from apps.api.app.models.user import User


router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)


# 1. CREATE LOCATION

@router.post(
    "/",
    response_model=LocationResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_location(
    location_data: LocationCreate,
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    return await LocationService.create_location(
        session,
        location_data
    )


# 2. GET ALL LOCATIONS

@router.get(
    "/",
    response_model=list[LocationResponse]
)
async def list_locations(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    return await LocationService.get_all_locations(
        session,
        skip=skip,
        limit=limit
    )


# 3. GET LOCATION BY ID

@router.get(
    "/{location_id}",
    response_model=LocationResponse
)
async def get_location_details(
    location_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    try:
        return await LocationService.get_location_by_id(
            session,
            location_id
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
