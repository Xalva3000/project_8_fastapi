from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Product
from sqlalchemy.engine import Result
from sqlalchemy import select
from src.product.schemas import ProductCreate, ProductUpdate, ProductUpdatePartial
from src.possession.schemas import PossessionCreate
from src.storage.schemas import StorageCreate
from src.possession import crud
from src.storage import crud


async def insert_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.dict())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    possession_in = PossessionCreate(product_id=product.product_id)
    await crud.insert_possession(session=session, possession_in=possession_in)
    storage_in = StorageCreate(product_id=product.product_id)
    await crud.insert_storage(session=session, storage_in=storage_in)
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
