# #src/db_utils.py
# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import HTTPException
# from src.db import async_session
from src.models.user import User

# async def get_user_from_database(user_id: int) -> User:
#     async with async_session() as session:
#         async with session.begin():
#             query = select(User).filter(User.id == user_id)
#             result = await session.execute(query)
#             user = result.scalars().first()
#             return user


from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_from_database(user_id: int, db: AsyncSession) -> User:
    async with db() as session:
        result = await session.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        return user
