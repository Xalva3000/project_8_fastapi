from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import StorageItem
from sqlalchemy.engine import Result
from sqlalchemy import select
from src.storage.schemas import StorageItemCreate, StorageItemUpdate, StorageItemUpdatePartial


async def insert_storage_item(session: AsyncSession, storage_item_in: StorageItemCreate) -> StorageItem:
    storage_item = StorageItem(**storage_item_in.dict())
    session.add(storage_item)
    await session.commit()
    await session.refresh(storage_item)
    return storage_item


async def select_all_storage_items(session: AsyncSession) -> list[StorageItem]:
    stmt = select(StorageItem).order_by(StorageItem.product_id)
    result: Result = await session.execute(stmt)
    storage_items = result.scalars().all()
    return storage_items


async def select_storage_item_by_id(session: AsyncSession, product_id: int) -> StorageItem | None:
    return await session.get(StorageItem, product_id)


async def select_available_storage_items(session: AsyncSession) -> list[StorageItem]:
    stmt = select(StorageItem).where(StorageItem.available != 0).order_by(StorageItem.product_id)
    result: Result = await session.execute(stmt)
    storage_items = result.scalars().all()
    return storage_items


async def delete_storage_item(session: AsyncSession, storage_item: StorageItem):
    await session.delete(storage_item)
    await session.commit()


async def update_storage_item(
        session: AsyncSession,
        storage_item: StorageItem,
        storage_item_update: StorageItemUpdate | StorageItemUpdatePartial,
        partial: bool = False
):
    for k, v in storage_item_update.model_dump(exclude_unset=partial).items():
        setattr(storage_item, k, v)
    await session.commit()
    return storage_item
