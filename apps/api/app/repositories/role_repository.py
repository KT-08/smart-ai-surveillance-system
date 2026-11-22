
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.app.models.role import Role


async def get_role_by_name(
    session: AsyncSession,
    role_name: str
):
    result = await session.execute(
        select(Role).where(Role.name == role_name)
    )

    return result.scalar_one_or_none()


async def get_role_by_id(
    session: AsyncSession,
    role_id: UUID
):
    result = await session.execute(
        select(Role).where(Role.id == role_id)
    )

    return result.scalar_one_or_none()


async def get_all_roles(
    session: AsyncSession
):
    result = await session.execute(
        select(Role).order_by(Role.name)
    )

    return result.scalars().all()
