from typing import Annotated

from fastapi import Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.connect import db_connect
from src.specification import crud
from src.specification.schemas import Specification


async def specification_by_id(
        specification_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> Specification:
    specification = await crud.select_specification_by_id(session=session, specification_id=specification_id)
    if specification is not None:
        return specification
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Specification {specification_id} not found"
    )
