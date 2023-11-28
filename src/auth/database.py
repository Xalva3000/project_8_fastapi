from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from src.config import settings
from src.database.models import role

DATABASE_URL = settings.load_driver_url(dbs="postgresql", driver="asyncpg")
Base: DeclarativeMeta = declarative_base()


class ApiUser(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'api_user'

    id = Column(Integer, primary_key=True)
    email = Column('email', String, nullable=False)
    username = Column('username', String, nullable=False)
    registered_at = Column('registered_at', TIMESTAMP, default=datetime.utcnow)
    role_id = Column('role_id', Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=True, nullable=False)
    is_verified: bool = Column(Boolean, default=True, nullable=False)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, ApiUser)
