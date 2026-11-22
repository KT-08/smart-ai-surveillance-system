
import asyncio

from sqlalchemy import select

from apps.api.app.db.session import AsyncSessionLocal
from apps.api.app.models.role import Role


async def seed_roles():
    predefined_roles = [
        "admin",
        "security"
    ]

    async with AsyncSessionLocal() as session:
        for role_name in predefined_roles:

            result = await session.execute(
                select(Role).where(Role.name == role_name)
            )

            existing_role = result.scalar_one_or_none()

            if existing_role is None:
                new_role = Role(name=role_name)
                session.add(new_role)
                print(f"Created role: {role_name}")

            else:
                print(f"Role already exists: {role_name}")

        await session.commit()

    print("Role seeding completed!")


if __name__ == "__main__":
    asyncio.run(seed_roles())
