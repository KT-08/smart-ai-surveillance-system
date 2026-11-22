
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.models.user import User


async def get_user_by_email(
    session: AsyncSession,
    email: str
):
    result = await session.execute(
        select(User).where(User.email == email)
    )

    return result.scalar_one_or_none()


async def get_user_by_id(
    session: AsyncSession,
    user_id: UUID
):
    result = await session.execute(
        select(User).where(User.id == user_id)
    )

    return result.scalar_one_or_none()


async def get_all_users(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 50
):
    result = await session.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return result.scalars().all()


async def create_user(
    session: AsyncSession,
    user: User
):
    session.add(user)

    await session.flush()
    await session.refresh(user)

    return user


async def update_user_status(
    session: AsyncSession,
    user: User,
    is_active: bool
):
    user.is_active = is_active

    await session.flush()
    await session.refresh(user)

    return user
