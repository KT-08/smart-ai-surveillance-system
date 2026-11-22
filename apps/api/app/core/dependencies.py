
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.db.session import get_db
from apps.api.app.repositories import user_repository
from apps.api.app.repositories import role_repository
from apps.api.app.core.security import decode_access_token


# Extract Bearer token from Authorization header
bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db)
):
    """
    Identify the currently authenticated user.
    """

    # 1. Extract token
    token = credentials.credentials

    # 2. Decode and verify JWT
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 3. Extract user ID
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 4. Validate UUID
    try:
        user_uuid = UUID(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 5. Retrieve user from database
    user = await user_repository.get_user_by_id(
        session,
        user_uuid
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 6. Check account status
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


def require_role(required_role: str):
    """
    Check whether the authenticated user has the required role.
    """

    async def role_checker(
        current_user=Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
    ):

        role = await role_repository.get_role_by_id(
            session,
            current_user.role_id
        )

        if role is None or role.name != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return current_user

    return role_checker
