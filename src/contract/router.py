from typing import Union

from fastapi import APIRouter, HTTPException, status, Depends
from src.contract import crud
from src.contract.schemas import Contract, ContractCreate, ContractUpdate, ContractUpdatePartial
from src.database.connect import db_connect
from src.contract.dependencies import contract_by_id
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=['Contracts'])


@router.get('/', response_model=Union[list[Contract], dict])
async def get_all_contracts(
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    result = await crud.select_all_contracts(session=session)
    if result:
        return result
    return "No contracts yet"


@router.post('/',
             response_model=Contract,
             status_code=status.HTTP_201_CREATED)
async def create_contract(
        contract_in: ContractCreate,
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.insert_contract(session, contract_in)


@router.get('/{contract_id}', response_model=Contract)
async def get_contract_by_id(contract: Contract = Depends(contract_by_id)):
    return contract


@router.delete('/{contract_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(
        contract: Contract = Depends(contract_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> None:
    await crud.delete_contract(session=session, contract=contract)


@router.put("/{contract_id}")
async def update_contract(
        contract_update: ContractUpdate,
        contract: Contract = Depends(contract_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_contract(
        session=session,
        contract=contract,
        contract_update=contract_update,
    )


@router.patch("/{contract_id}")
async def update_contract_partial(
        contract_update: ContractUpdatePartial,
        contract: Contract = Depends(contract_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_contract(
        session=session,
        contract=contract,
        contract_update=contract_update,
        partial=True,
    )
