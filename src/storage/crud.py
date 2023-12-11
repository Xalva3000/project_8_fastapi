from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Storage
from sqlalchemy.engine import Result
from sqlalchemy import select
from src.storage.schemas import StorageCreate, StorageUpdate, StorageUpdatePartial


async def insert_storage(session: AsyncSession, storage_in: StorageCreate) -> Storage:
    storage = Storage(**storage_in.dict())
    session.add(storage)
    await session.commit()
    await session.refresh(storage)
    return storage


async def select_all_storages(session: AsyncSession) -> list[Storage]:
    stmt = select(Storage).order_by(Storage.product_id)
    result: Result = await session.execute(stmt)
    storages = result.scalars().all()
    return storages


async def select_storage_by_id(session: AsyncSession, product_id: int) -> Storage | None:
    return await session.get(Storage, product_id)


async def select_no_zero_storage(session: AsyncSession) -> list[Storage]:
    stmt = select(Storage).where(Storage.quantity != 0).order_by(Storage.product_id)
    result: Result = await session.execute(stmt)
    storages = result.scalars().all()
    return storages


async def delete_storage(session: AsyncSession, storage: Storage):
    await session.delete(storage)
    await session.commit()


async def update_storage(
        session: AsyncSession,
        storage: Storage,
        storage_update: StorageUpdate | StorageUpdatePartial,
        partial: bool = False
):
    for k, v in storage_update.model_dump(exclude_unset=partial).items():
        setattr(storage, k, v)
    await session.commit()
    return storage
