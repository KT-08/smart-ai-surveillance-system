
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.db.session import get_db
from apps.api.app.schemas.user import UserLogin, UserResponse
from apps.api.app.models.user import User
from apps.api.app.repositories import user_repository
from apps.api.app.repositories import role_repository
from apps.api.app.core.security import (
    verify_password,
    create_access_token
)
from apps.api.app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
async def login(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_db)
):
    """
    Authenticate Admin or Security Personnel.
    """

    # 1. Find user using email
    user = await user_repository.get_user_by_email(
        session,
        login_data.email
    )

    # 2. Verify user and password
    if user is None or not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. Check whether account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # 4. Retrieve user's role
    role = await role_repository.get_role_by_id(
        session,
        user.role_id
    )

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role not found"
        )

    # 5. Generate JWT access token
    access_token = create_access_token({
        "sub": str(user.id)
    })

    # 6. Return token and safe user information
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": role.name,
            "is_active": user.is_active
        }
    }


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Return details of the currently authenticated user.
    """

    return current_user
