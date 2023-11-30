from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker, async_scoped_session, AsyncSession)
from src.database.config import PSQLConfig
from asyncio import current_task


class DBConnect:
    def __init__(self, driver_url: str, echo: bool = False):
        self.engine = create_async_engine(url=driver_url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        async with session() as sess:
            yield sess
            await session.remove()


settings = PSQLConfig('.env')

db_connect = DBConnect(
    driver_url=settings.load_driver_url(
        dbs='postgresql',
        driver='asyncpg'),
    echo=True
)
