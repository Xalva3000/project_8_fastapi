from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Contractor
from sqlalchemy.engine import Result
from sqlalchemy import select
from src.contractor.schemas import ContractorCreate, ContractorUpdate, ContractorUpdatePartial


async def insert_contractor(session: AsyncSession, contractor_in: ContractorCreate) -> Contractor:
    contractor = Contractor(**contractor_in.dict())
    session.add(contractor)
    await session.commit()
    await session.refresh(contractor)
    return contractor


async def select_all_contractors(session: AsyncSession) -> list[Contractor]:
    stmt = select(Contractor).order_by(Contractor.contractor_id)
    result: Result = await session.execute(stmt)
    contractors = result.scalars().all()
    return contractors


async def select_contractor_by_id(session: AsyncSession, contractor_id: int) -> Contractor | None:
    return await session.get(Contractor, contractor_id)


async def delete_contractor(session: AsyncSession, contractor: Contractor):
    await session.delete(contractor)
    await session.commit()


async def update_contractor(
        session: AsyncSession,
        contractor: Contractor,
        contractor_update: ContractorUpdate | ContractorUpdatePartial,
        partial: bool = False
):
    for k, v in contractor_update.model_dump(exclude_unset=partial).items():
        setattr(contractor, k, v)
    await session.commit()
    return contractor
