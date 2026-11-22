
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.repositories import user_repository
from apps.api.app.repositories import role_repository
from apps.api.app.core.security import hash_password
from apps.api.app.models.user import User


# --------------------------------------------------
# 1. CREATE SECURITY USER
# --------------------------------------------------

async def create_security_user(
    session: AsyncSession,
    name: str,
    email: str,
    password: str
):
    """
    Create a Security Personnel account.
    """

    existing_user = await user_repository.get_user_by_email(
        session,
        email
    )

    if existing_user is not None:
        raise ValueError("Email is already registered")

    security_role = await role_repository.get_role_by_name(
        session,
        "security"
    )

    if security_role is None:
        raise ValueError("Security role not found")

    hashed_password = hash_password(password)

    new_user = User(
        name=name,
        email=email,
        password_hash=hashed_password,
        role_id=security_role.id
    )

    created_user = await user_repository.create_user(
        session,
        new_user
    )

    await session.commit()

    return created_user


# --------------------------------------------------
# 2. GET ALL USERS
# --------------------------------------------------

async def get_users(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 50
):
    return await user_repository.get_all_users(
        session,
        skip,
        limit
    )


# --------------------------------------------------
# 3. GET USER BY ID
# --------------------------------------------------

async def get_user(
    session: AsyncSession,
    user_id: UUID
):
    return await user_repository.get_user_by_id(
        session,
        user_id
    )


# --------------------------------------------------
# 4. UPDATE USER ACTIVE STATUS
# --------------------------------------------------

async def change_user_status(
    session: AsyncSession,
    user_id: UUID,
    is_active: bool
):
    """
    Activate or deactivate a user account.
    """

    user = await user_repository.get_user_by_id(
        session,
        user_id
    )

    if user is None:
        raise ValueError("User not found")

    user = await user_repository.update_user_status(
        session,
        user,
        is_active
    )

    await session.commit()

    return user
