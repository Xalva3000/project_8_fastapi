from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.specification.dependencies import specification_by_id
from src.specification.schemas import Specification, SpecificationCreate, SpecificationUpdate, \
    SpecificationUpdatePartial, ContractSpecificationsCreate
from src.database.connect import db_connect
from src.specification import crud

router = APIRouter(tags=['Specifications'])


@router.post('/',
             response_model=Specification,
             status_code=status.HTTP_201_CREATED)
async def create_specification(
        specification_in: SpecificationCreate,
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.insert_specification(session, specification_in)


@router.post('/contract/{contract_id}',
             response_model=list[Specification],
             status_code=status.HTTP_201_CREATED)
async def create_specifications(
        contract_id: int,
        specifications_in: ContractSpecificationsCreate,
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.insert_specifications(session, contract_id, specifications_in)


@router.get('/', response_model=list[Specification])
async def get_all_specifications(
        session: AsyncSession = Depends(db_connect.session_dependency),
):
    return await crud.select_all_specifications(session=session)


@router.get('/{specification_id}', response_model=Specification)
async def get_specification_by_id(specification: Specification = Depends(specification_by_id)):
    return specification


@router.get('/contract/{contract_id}', response_model=list[Specification])
async def get_specifications_by_contract_id(contract_id: int,
                                            session: AsyncSession = Depends(db_connect.session_dependency)):
    return await crud.select_specifications_by_contract_id(session=session, contract_id=contract_id)


@router.delete('/contract/{contract_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_specifications_by_contract_id(
        contract_id: int,
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> None:
    await crud.delete_specifications_by_contract_id(session=session, contract_id=contract_id)


@router.delete('/{specification_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_specification(
        specification: Specification = Depends(specification_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency),
) -> None:
    await crud.delete_specification(session=session, specification=specification)


@router.put("/{specification_id}")
async def update_specification(
        specification_update: SpecificationUpdate,
        specification: Specification = Depends(specification_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_specification(
        session=session,
        specification=specification,
        specification_update=specification_update,
    )


@router.patch("/{specification_id}")
async def update_specification_partial(
        specification_update: SpecificationUpdatePartial,
        specification: Specification = Depends(specification_by_id),
        session: AsyncSession = Depends(db_connect.session_dependency)
):
    return await crud.update_specification(
        session=session,
        specification=specification,
        specification_update=specification_update,
        partial=True,
    )
