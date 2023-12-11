from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contract
from src.specification.crud import select_specifications_by_contract_id
from src.possession import crud
from src.storage import crud


async def confirm_contract_payment(session: AsyncSession, contract: Contract):
    if not contract.payment:
        contract.payment = True
        await session.commit()
    return contract


async def increase_possession(session: AsyncSession, contract: Contract):
    specifications = await select_specifications_by_contract_id(session=session, contract_id=contract.contract_id)
    for spec in specifications:
        possession = await crud.select_possession_by_id(session=session, product_id=spec.product_id)
        possession.quantity += spec.quantity
    await session.commit()
    result = await crud.select_no_zero_possession(session=session)
    return result


async def decrease_possession(session: AsyncSession, contract: Contract):
    specifications = await select_specifications_by_contract_id(session=session, contract_id=contract.contract_id)
    for spec in specifications:
        possession = await crud.select_possession_by_id(session=session, product_id=spec.product_id)
        possession.quantity -= spec.quantity
    await session.commit()
    result = await crud.select_no_zero_possession(session=session)
    return result


async def confirm_contract_execution(session: AsyncSession, contract: Contract):
    if not contract.executed:
        contract.executed = True
        await session.commit()
    return contract


async def increase_storage(session: AsyncSession, contract: Contract):
    specifications = await select_specifications_by_contract_id(session=session, contract_id=contract.contract_id)
    for spec in specifications:
        storage = await crud.select_storage_by_id(session=session, product_id=spec.product_id)
        storage.quantity += spec.quantity
    await session.commit()
    result = await crud.select_no_zero_storage(session=session)
    return result


async def decrease_storage(session: AsyncSession, contract: Contract):
    specifications = await select_specifications_by_contract_id(session=session, contract_id=contract.contract_id)
    for spec in specifications:
        storage = await crud.select_storage_by_id(session=session, product_id=spec.product_id)
        storage.quantity -= spec.quantity
    await session.commit()
    result = await crud.select_no_zero_storage(session=session)
    return result
