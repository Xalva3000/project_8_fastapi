from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Specification
from sqlalchemy.engine import Result
from sqlalchemy import select, delete
from src.specification.schemas import SpecificationCreate, SpecificationUpdate, SpecificationUpdatePartial, \
    ContractSpecificationsCreate


async def insert_specification(session: AsyncSession, specification_in: SpecificationCreate) -> Specification:
    specification = Specification(**specification_in.dict())
    session.add(specification)
    await session.commit()
    await session.refresh(specification)
    return specification


async def insert_specifications(
        session: AsyncSession,
        contract_id: int,
        new_positions: ContractSpecificationsCreate
) -> list[Specification]:
    specifications = [Specification(**specification_in.dict(), contract_id=contract_id) for specification_in in
                      new_positions.specifications]
    session.add_all(specifications)
    await session.commit()
    contract_specifications = await select_specifications_by_contract_id(session=session, contract_id=contract_id)
    return contract_specifications


async def select_all_specifications(session: AsyncSession) -> list[Specification]:
    stmt = select(Specification).order_by(Specification.product_id)
    result: Result = await session.execute(stmt)
    specifications = result.scalars().all()
    return specifications


async def select_specifications_by_contract_id(session: AsyncSession, contract_id: int) -> list[Specification]:
    stmt = select(Specification).where(Specification.contract_id == contract_id)
    result: Result = await session.execute(stmt)
    specifications = result.scalars().all()
    return specifications


async def select_specification_by_id(session: AsyncSession, product_id: int) -> Specification | None:
    return await session.get(Specification, product_id)


async def delete_specification(session: AsyncSession, specification: Specification):
    await session.delete(specification)
    await session.commit()


async def delete_specifications_by_contract_id(session: AsyncSession, contract_id: int):
    stmt = delete(Specification).where(Specification.contract_id == contract_id)
    await session.execute(stmt)
    await session.commit()


async def update_specification(
        session: AsyncSession,
        specification: Specification,
        specification_update: SpecificationUpdate | SpecificationUpdatePartial,
        partial: bool = False
):
    for k, v in specification_update.model_dump(exclude_unset=partial).items():
        setattr(specification, k, v)
    await session.commit()
    return specification
