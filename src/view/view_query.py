from datetime import datetime
from typing import Optional
from datetime import date

from sqlalchemy import select, desc, Result, cast, DATE, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.database.models import Contract, Specification, StorageItem, Contractor
from src.view.view_scheme import ContractFilter


async def select_no_payment_contracts(session: AsyncSession):
    stmt = select(Contract).where(Contract.payment == False)
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_not_executed_contracts(session: AsyncSession):
    stmt = select(Contract).where(Contract.executed == False)
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_income_contracts(session: AsyncSession):
    stmt = select(Contract).where(Contract.deleted_at == None).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).filter(Contract.contract_type == 'income').order_by(desc(Contract.contract_id))
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_outcome_contracts(session: AsyncSession):
    stmt = select(Contract).where(Contract.deleted_at == None).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).filter(Contract.contract_type == 'outcome').order_by(desc(Contract.contract_id))
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_no_execution_contracts(session: AsyncSession):
    stmt = select(Contract).where(and_(Contract.executed.is_(False), Contract.deleted_at == None)).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).order_by(desc(Contract.contract_id))
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_deleted_contracts(session: AsyncSession):
    stmt = select(Contract).where(Contract.deleted_at != None).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).order_by(desc(Contract.contract_id))
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_today_contracts(session: AsyncSession):
    stmt = select(Contract).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).filter(and_(or_(
        cast(Contract.executed_at, DATE) == date.today(),
        cast(Contract.created_at, DATE) == date.today()),
        Contract.deleted_at == None)).order_by(
        desc(Contract.contract_id))
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_contracts_on_date(session: AsyncSession, user_date: str):
    stmt = select(Contract).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).filter(and_(cast(Contract.planned_date, DATE) == datetime.strptime(user_date, "%Y-%m-%d"),
                  Contract.deleted_at == None)).order_by(
        desc(Contract.contract_id))
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_full_contracts(session: AsyncSession):
    stmt = select(Contract).where(Contract.deleted_at == None).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).order_by(desc(Contract.contract_id))

    result: Result = await session.execute(stmt)
    contracts = result.scalars().all()
    return contracts


async def select_contracts_by_idlist(session: AsyncSession, id_list: list[int]):
    stmt = select(Contract).where(and_(Contract.contract_id.in_(id_list), Contract.deleted_at == None)).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).order_by(desc(Contract.contract_id))

    result: Result = await session.execute(stmt)
    contracts = result.scalars().all()
    return contracts


async def select_full_contract_by_id(session: AsyncSession, contract_id: int):
    stmt = select(Contract).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).filter(and_(Contract.contract_id == contract_id, Contract.deleted_at == None))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def select_full_contracts_by_contractor_id(session: AsyncSession, contractor_id: int):
    stmt = select(Contract).where(
        and_(Contract.deleted_at == None,
             Contract.contractor_id == contractor_id)).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).order_by(desc(Contract.contract_id))

    result: Result = await session.execute(stmt)
    contracts = result.scalars().all()
    return contracts


async def select_full_contracts_by_product_id(session: AsyncSession, product_id: int):
    stmt = select(Contract).where(Contract.deleted_at == None).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).filter(Contract.specifications.any(Specification.product_id == product_id)).order_by(desc(Contract.contract_id))
    result: Result = await session.execute(stmt)
    contracts = result.scalars().all()
    return contracts


async def select_contacts_with_contractor(session: AsyncSession):
    stmt = select(Contract).options(joinedload(Contract.contractor)).order_by(Contract.contract_id)
    result = await session.scalars(stmt)
    return result


async def select_contracts_with_specifications(session: AsyncSession):
    stmt = select(Contract).where(
        Contract.deleted_at == None
    ).options(
        selectinload(Contract.specifications)
    ).order_by(Contract.contract_id)
    result: Result = await session.execute(stmt)
    contracts = result.scalars()
    return contracts


async def select_contract_by_id_with_specifications(session: AsyncSession, contract_id: int) -> Optional[Contract]:
    stmt = select(Contract).options(
        joinedload(Contract.contractor),
        selectinload(Contract.specifications).joinedload(Specification.product),
    ).where(Contract.contract_id == contract_id)
    result: Result = await session.execute(stmt)
    contract = result.scalar_one_or_none()
    return contract


async def select_contactor_with_contracts(session: AsyncSession):
    stmt = select(Contractor).options(joinedload(Contractor.contracts)).order_by(Contractor.contractor_id)
    result = await session.scalars(stmt)
    return result


async def select_storage_items_with_products(session: AsyncSession):
    stmt = select(StorageItem).options(joinedload(StorageItem.product)).order_by(StorageItem.product_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_nonzero_storage_items_with_products(session: AsyncSession):
    stmt = select(StorageItem) \
        .where((StorageItem.available != 0) | (StorageItem.owned != 0) | (StorageItem.stored != 0)) \
        .options(joinedload(StorageItem.product)) \
        .order_by(StorageItem.product_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_free_to_sell_storage_items_with_products(session: AsyncSession):
    stmt = select(StorageItem) \
        .where(StorageItem.available != 0) \
        .options(joinedload(StorageItem.product)) \
        .order_by(StorageItem.product_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_owned_storage_items_with_products(session: AsyncSession):
    stmt = select(StorageItem) \
        .where(StorageItem.owned != 0) \
        .options(joinedload(StorageItem.product)) \
        .order_by(StorageItem.product_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_stored_storage_items_with_products(session: AsyncSession):
    stmt = select(StorageItem) \
        .where(StorageItem.stored != 0) \
        .options(joinedload(StorageItem.product)) \
        .order_by(StorageItem.product_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def select_storage_item_by_product_id(session: AsyncSession, product_id: int):
    stmt = select(StorageItem).where(StorageItem.product_id == product_id)
    result = await session.scalar(stmt)
    return result


# async def select_filtered_contracts(filter: ContractFilter, session: AsyncSession):
#     query = filter.filter(select(Contract).options(
#         joinedload(Contract.contractor),
#         selectinload(Contract.specifications).joinedload(Specification.product),
#     ).order_by(desc(Contract.contract_id)))
#     result = await session.execute(query)
#     return result.scalars().all()


async def select_filtered_contracts(filter: ContractFilter, session: AsyncSession):
    query = filter.filter(
        select(Contract.contract_id).where(Contract.deleted_at == None).outerjoin(Specification).distinct(
            Contract.contract_id))
    result = await session.execute(query)
    return result.scalars().all()
