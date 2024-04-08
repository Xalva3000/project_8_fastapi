from typing import Annotated

from fastapi import Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.connect import db_connect
from src.storage import crud
from src.storage.schemas import StorageItem


async def storage_item_by_id(
        product_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> StorageItem:
    storage_item = await crud.select_storage_item_by_id(session=session, product_id=product_id)
    if storage_item is not None:
        return storage_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"StorageItem {product_id} not found"
    )
