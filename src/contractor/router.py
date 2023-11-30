from fastapi import APIRouter, HTTPException, status, Depends
from src.contractor import crud
from src.contractor.schemas import Contractor, ContractorCreate, ContractorUpdate, ContractorUpdatePartial
from src.database.connect import db_connect
from src.contractor.dependencies import contractor_by_id
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=['Contractors'])


@router.get('/', response_model=list[Contractor])
async def get_all_contractors(
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.select_all_contractors(session=session)


@router.post('/',
             response_model=Contractor,
             status_code=status.HTTP_201_CREATED)
async def create_contractor(
        contractor_in: ContractorCreate,
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.insert_contractor(session, contractor_in)


@router.get('/{contractor_id}', response_model=Contractor)
async def get_contractor_by_id(contractor: Contractor = Depends(contractor_by_id)):
    return contractor


@router.delete('/{contractor_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contractor(
        contractor: Contractor = Depends(contractor_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> None:
    await crud.delete_contractor(session=session, contractor=contractor)


@router.put("/{contractor_id}")
async def update_contractor(
        contractor_update: ContractorUpdate,
        contractor: Contractor = Depends(contractor_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_contractor(
        session=session,
        contractor=contractor,
        contractor_update=contractor_update,
    )


@router.patch("/{contractor_id}")
async def update_contractor_partial(
        contractor_update: ContractorUpdatePartial,
        contractor: Contractor = Depends(contractor_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_contractor(
        session=session,
        contractor=contractor,
        contractor_update=contractor_update,
        partial=True,
    )
