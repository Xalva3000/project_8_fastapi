from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.dependencies import storage_by_id
from src.storage.schemas import Storage, StorageCreate, StorageUpdate, StorageUpdatePartial
from src.database.connect import db_connect
from src.storage import crud

router = APIRouter(tags=['Storage'])


@router.get('/', response_model=list[Storage])
async def get_all_storages(
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.select_all_storages(session=session)


@router.post('/',
             response_model=Storage,
             status_code=status.HTTP_201_CREATED)
async def create_storage(
        storage_in: StorageCreate,
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.insert_storage(session, storage_in)


@router.get('/{storage_id}', response_model=Storage)
async def get_storage_by_id(storage: Storage = Depends(storage_by_id)):
    return storage


@router.delete('/{storage_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_storage(
        storage: Storage = Depends(storage_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> None:
    await crud.delete_storage(session=session, storage=storage)


@router.put("/{storage_id}")
async def update_storage(
        storage_update: StorageUpdate,
        storage: Storage = Depends(storage_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_storage(
        session=session,
        storage=storage,
        storage_update=storage_update,
    )


@router.patch("/{storage_id}")
async def update_storage_partial(
        storage_update: StorageUpdatePartial,
        storage: Storage = Depends(storage_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_storage(
        session=session,
        storage=storage,
        storage_update=storage_update,
        partial=True,
    )
