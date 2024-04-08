from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.dependencies import storage_item_by_id
from src.storage.schemas import StorageItem, StorageItemCreate, StorageItemUpdate, StorageItemUpdatePartial
from src.database.connect import db_connect
from src.storage import crud

router = APIRouter(tags=['StorageItem'])


@router.get('/', response_model=list[StorageItem])
async def get_all_storage_items(
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.select_all_storage_items(session=session)


@router.post('/',
             response_model=StorageItem,
             status_code=status.HTTP_201_CREATED)
async def create_storage_item(
        storage_item_in: StorageItemCreate,
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.insert_storage_item(session, storage_item_in)


@router.get('/{storage_item_id}', response_model=StorageItem)
async def get_storage_item_by_id(storage_item: StorageItem = Depends(storage_item_by_id)):
    return storage_item


@router.delete('/{storage_item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_storage_item(
        storage_item: StorageItem = Depends(storage_item_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> None:
    await crud.delete_storage_item(session=session, storage_item=storage_item)


@router.put("/{storage_item_id}")
async def update_storage_item(
        storage_item_update: StorageItemUpdate,
        storage_item: StorageItem = Depends(storage_item_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_storage_item(
        session=session,
        storage_item=storage_item,
        storage_item_update=storage_item_update,
    )


@router.patch("/{storage_item_id}")
async def update_storage_item_partial(
        storage_item_update: StorageItemUpdatePartial,
        storage_item: StorageItem = Depends(storage_item_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_storage_item(
        session=session,
        storage_item=storage_item,
        storage_item_update=storage_item_update,
        partial=True,
    )
