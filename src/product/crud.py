from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Product
from sqlalchemy.engine import Result
from sqlalchemy import select
from src.product.schemas import ProductCreate, ProductUpdate, ProductUpdatePartial
from src.storage.schemas import StorageItemCreate
from src.storage.crud import insert_storage_item


async def insert_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.dict())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    storage_item_in = StorageItemCreate(product_id=product.product_id)
    await insert_storage_item(session=session, storage_item_in=storage_item_in)
    return product


async def select_all_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.product_id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return products


async def select_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def delete_product(session: AsyncSession, product: Product):
    await session.delete(product)
    await session.commit()


async def update_product(
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate | ProductUpdatePartial,
        partial: bool = False
):
    for k, v in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, k, v)
    await session.commit()
    return product
