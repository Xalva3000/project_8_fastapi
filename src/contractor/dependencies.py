from typing import Annotated

from fastapi import Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.connect import db_connect
from src.contractor import crud
from src.contractor.schemas import Contractor


async def contractor_by_id(
        contractor_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> Contractor:
    contractor = await crud.select_contractor_by_id(session=session, contractor_id=contractor_id)
    if contractor is not None:
        return contractor
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Contractor {contractor_id} not found"
    )
