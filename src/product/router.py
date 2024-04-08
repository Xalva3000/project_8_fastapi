from fastapi import APIRouter, HTTPException, status, Depends
from src.product import crud
from src.product.schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from src.database.connect import db_connect
from src.product.dependencies import product_by_id
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=['Products'])


@router.get('/', response_model=list[Product])
async def get_all_products(
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.select_all_products(session=session)


@router.post('/',
             response_model=Product,
             status_code=status.HTTP_201_CREATED)
async def create_product(
        product_in: ProductCreate,
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.insert_product(session, product_in)


@router.get('/{product_id}', response_model=Product)
async def get_product_by_id(product: Product = Depends(product_by_id)):
    return product


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> None:
    await crud.delete_product(session=session, product=product)


@router.put("/{product_id}")
async def update_product(
        product_update: ProductUpdate,
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch("/{product_id}")
async def update_product_partial(
        product_update: ProductUpdatePartial,
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )
