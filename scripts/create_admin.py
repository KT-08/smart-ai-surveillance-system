
import asyncio
from getpass import getpass

from pydantic import TypeAdapter, EmailStr, ValidationError
from sqlalchemy import select, func

from apps.api.app.db.session import AsyncSessionLocal
from apps.api.app.models.user import User
from apps.api.app.models.role import Role
from apps.api.app.core.security import hash_password


email_validator = TypeAdapter(EmailStr)


async def create_initial_admin():
    print("\n=== Initial Admin Setup ===\n")

    async with AsyncSessionLocal() as session:
        async with session.begin():

            # 1. Check whether an Admin already exists
            admin_role_result = await session.execute(
                select(Role).where(Role.name == "admin")
            )
            admin_role = admin_role_result.scalar_one_or_none()

            if admin_role is None:
                print("Admin role not found. Run seed_roles first.")
                return

            existing_admin_result = await session.execute(
                select(func.count(User.id)).where(
                    User.role_id == admin_role.id
                )
            )

            if existing_admin_result.scalar_one() > 0:
                print("An Admin account already exists.")
                print("Initial setup is not allowed again.")
                return

            # 2. Collect Admin information
            name = input("Enter Admin name: ").strip()
            email = input("Enter Admin email: ").strip().lower()

            if not name or not email:
                print("Name and email are required.")
                return

            # 3. Validate email format
            try:
                email = str(email_validator.validate_python(email))
            except ValidationError:
                print("Invalid email format. Please enter a valid email.")
                return

            # 4. Collect and validate password
            password = getpass("Enter Admin password: ")
            confirm_password = getpass("Confirm Admin password: ")

            if password != confirm_password:
                print("Passwords do not match.")
                return

            if len(password) < 12:
                print("Password must contain at least 12 characters.")
                return

            # 5. Check email uniqueness
            email_result = await session.execute(
                select(User).where(User.email == email)
            )

            if email_result.scalar_one_or_none() is not None:
                print("This email is already registered.")
                return

            # 6. Hash password
            hashed_password = hash_password(password)

            # 7. Create Admin account
            admin = User(
                name=name,
                email=email,
                password_hash=hashed_password,
                role_id=admin_role.id
            )

            session.add(admin)

        print("\nInitial Admin account created successfully!")


if __name__ == "__main__":
    asyncio.run(create_initial_admin())
