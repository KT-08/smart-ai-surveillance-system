import asyncio
from sqlalchemy import text
from apps.api.app.db.session import engine


async def test_connection():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            print("Database connected successfully!")
            print("Test result:", result.scalar())

    except Exception as error:
        print("Database connection failed!")
        print("Error:", error)

    finally:
        await engine.dispose()


asyncio.run(test_connection())