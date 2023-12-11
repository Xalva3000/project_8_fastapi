from typing import Annotated

from fastapi import Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.connect import db_connect
from src.possession import crud
from src.possession.schemas import Possession


async def possession_by_id(
        product_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> Possession:
    possession = await crud.select_possession_by_id(session=session, product_id=product_id)
    if possession is not None:
        return possession
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found in possession"
    )
