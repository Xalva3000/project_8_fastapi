from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.contract.dependencies import contract_by_id
from src.database.connect import db_connect
from src.database.models import Contract
from src.contract import execution_query

router = APIRouter(tags=['Execution'])


@router.patch("/{contract_id}/payment")
async def confirm_payment(contract: Contract = Depends(contract_by_id),
                          session: AsyncSession = Depends(db_connect.session_dependency)):
    if contract.payment:
        return contract
    if contract.contract_type == "income":
        await execution_query.increase_possession(session=session, contract=contract)
    else:
        await execution_query.decrease_possession(session=session, contract=contract)
    result = await execution_query.confirm_contract_payment(session=session, contract=contract)
    return result


@router.patch("/{contract_id}/execution")
async def confirm_execution(contract: Contract = Depends(contract_by_id),
                            session: AsyncSession = Depends(db_connect.session_dependency)):
    if contract.executed:
        return contract
    if contract.contract_type == "income":
        await execution_query.increase_storage(session=session, contract=contract)
    else:
        await execution_query.decrease_storage(session=session, contract=contract)
    result = await execution_query.confirm_contract_execution(session=session, contract=contract)
    return result

# """contract actions"""
# +confirm_payment
# confirm_execution
# +delete contract есть
# cancel payment
# cancel execution


# """specifications actions"""
# +get specification by contract id
# +delete specifications by contract id
# +insert many specifications
