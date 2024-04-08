import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Product
from src.database.connect import db_connect
from src.product.schemas import ProductCreate
from src.view.view import get_filtered_contracts
from src.view.view_query import select_no_payment_contracts, select_today_contracts, select_no_execution_contracts, \
    select_nonzero_storage_items_with_products, select_storage_items_with_products, \
    select_contract_by_id_with_specifications, select_full_contracts, select_full_contracts_by_product_id


async def insert_product(session: AsyncSession, product_in: ProductCreate):
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return 'done'


async def main():
    # async with db_connect.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

    async with db_connect.session_factory() as session:
        #     result = await select_full_contracts(session=session)
        #
        #     for contract in result:
        #         print(contract.contractor, contract.contract_type, contract.reserve, contract.payment, contract.execute)
        #         for spec in contract.specifications:
        #             print(spec.product, spec.quantity, spec.quantity * spec.product.weight)

        # stmt = select(Product)
        # result = await session.execute(stmt)
        # print(result.scalars().all())
        # product_in = ProductCreate(fish='Сельдь',
        #                            cutting='НР',
        #                            size='400-600',
        #                            producer='Акрос',
        #                            package='короб',
        #                            weight=15)
        # result = await insert_product(session=session, product_in=product_in)

        # contracts = await select_full_contracts_by_product_id(session=session, product_id=7)
        # for contract in contracts:
        #     print(contract.contract_id)
        #     for spec in contract.specifications:
        #         print(spec.product)

        lst = await get_filtered_contracts()

        print(lst)


if __name__ == '__main__':
    asyncio.run(main())
