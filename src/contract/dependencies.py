from typing import Annotated

from fastapi import Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.connect import db_connect
from src.contract import crud
from src.contract.schemas import Contract


async def contract_by_id(
        contract_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> Contract:
    contract = await crud.select_contract_by_id(session=session, contract_id=contract_id)
    if contract is not None:
        return contract
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Contract {contract_id} not found"
    )
