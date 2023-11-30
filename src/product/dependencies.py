from typing import Annotated

from fastapi import Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.connect import db_connect
from src.product import crud
from src.product.schemas import Product


async def product_by_id(
        product_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> Product:
    product = await crud.select_product_by_id(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found"
    )
