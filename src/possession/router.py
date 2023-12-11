from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.possession.dependencies import possession_by_id
from src.possession.schemas import Possession, PossessionCreate, PossessionUpdate, PossessionUpdatePartial
from src.database.connect import db_connect
from src.possession import crud

router = APIRouter(tags=['Possessions'])


@router.get('/all/', response_model=list[Possession])
async def get_all_possessions(
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.select_all_possessions(session=session)


@router.get('/', response_model=list[Possession])
async def get_no_zero_possessions(
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.select_no_zero_possession(session=session)


@router.post('/',
             response_model=Possession,
             status_code=status.HTTP_201_CREATED)
async def create_possession(
        possession_in: PossessionCreate,
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.insert_possession(session, possession_in)


@router.get('/{product_id}', response_model=Possession)
async def get_possession_by_id(possession: Possession = Depends(possession_by_id)):
    return possession


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_possession(
        possession: Possession = Depends(possession_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> None:
    await crud.delete_possession(session=session, possession=possession)


@router.put("/{product_id}")
async def update_possession(
        possession_update: PossessionUpdate,
        possession: Possession = Depends(possession_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_possession(
        session=session,
        possession=possession,
        possession_update=possession_update,
    )


@router.patch("/{product_id}")
async def update_possession_partial(
        possession_update: PossessionUpdatePartial,
        possession: Possession = Depends(possession_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_possession(
        session=session,
        possession=possession,
        possession_update=possession_update,
        partial=True,
    )
