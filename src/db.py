# # src/db.py
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# # DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
# DATABASE_URL = "mysql://admin:Admin123@localhost/report_generator_db"

# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )

# Base = declarative_base()


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models.base import Base

DATABASE_URL = "mysql+asyncmy://admin:Admin123@localhost/report_generator_db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session
