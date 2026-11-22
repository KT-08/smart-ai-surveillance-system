
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.db.session import get_db
from apps.api.app.schemas.user import (
    UserCreate,
    UserResponse,
    UserStatusUpdate
)
from apps.api.app.services.user_service import (
    create_security_user,
    get_users,
    get_user,
    change_user_status
)
from apps.api.app.core.dependencies import require_role
from apps.api.app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# --------------------------------------------------
# 1. CREATE SECURITY ACCOUNT
# --------------------------------------------------

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_security_account(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    """
    Allow Admin to create a Security Personnel account.
    """

    try:
        new_user = await create_security_user(
            session=session,
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )

        return new_user

    except ValueError as error:
        message = str(error)

        if message == "Email is already registered":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create Security account"
        )


# --------------------------------------------------
# 2. VIEW ALL USERS
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[UserResponse]
)
async def list_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    """
    Allow Admin to view all registered users.
    """

    users = await get_users(
        session=session,
        skip=skip,
        limit=limit
    )

    return users


# --------------------------------------------------
# 3. VIEW USER BY ID
# --------------------------------------------------

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
async def get_user_details(
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    """
    Allow Admin to view a particular user by ID.
    """

    user = await get_user(
        session=session,
        user_id=user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


# --------------------------------------------------
# 4. ACTIVATE / DEACTIVATE USER
# --------------------------------------------------

@router.patch(
    "/{user_id}/status",
    response_model=UserResponse
)
async def update_user_status(
    user_id: UUID,
    status_data: UserStatusUpdate,
    session: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    """
    Allow Admin to activate or deactivate a user account.
    """

    try:
        updated_user = await change_user_status(
            session=session,
            user_id=user_id,
            is_active=status_data.is_active
        )

        return updated_user

    except ValueError as error:
        if str(error) == "User not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update user status"
        )
