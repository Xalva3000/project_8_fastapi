from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Contract
from sqlalchemy.engine import Result
from sqlalchemy import select
from src.contract.schemas import ContractCreate, ContractUpdate, ContractUpdatePartial


async def insert_contract(session: AsyncSession, contract_in: ContractCreate) -> Contract:
    contract = Contract(**contract_in.dict())
    session.add(contract)
    await session.commit()
    await session.refresh(contract)
    return contract


async def select_all_contracts(session: AsyncSession) -> list[Contract]:
    stmt = select(Contract).order_by(Contract.contract_id)
    result: Result = await session.execute(stmt)
    contracts = result.scalars().all()
    return contracts


async def select_contract_by_id(session: AsyncSession, contract_id: int) -> Contract | None:
    return await session.get(Contract, contract_id)


async def delete_contract(session: AsyncSession, contract: Contract):
    await session.delete(contract)
    await session.commit()


async def update_contract(
        session: AsyncSession,
        contract: Contract,
        contract_update: ContractUpdate | ContractUpdatePartial,
        partial: bool = False
):
    for k, v in contract_update.model_dump(exclude_unset=partial).items():
        setattr(contract, k, v)
    await session.commit()
    return contract
