from typing import Any

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connect import db_connect
from src.database.models import Contract
from src.view.view_query import select_no_payment_contracts, select_not_executed_contracts, select_full_contracts, \
    select_storage_items_with_products, select_deleted_contracts, select_filtered_contracts
from src.view.view_scheme import ContractFilter
from fastapi_pagination import Page, paginate, Params

router = APIRouter(tags=['view'])


@router.get("/no_payment_contracts/")
async def get_no_payment_contracts(session: AsyncSession = Depends(db_connect.session_dependency)):
    result = await select_no_payment_contracts(session=session)
    return result


@router.get("/not_executed_contracts/")
async def get_not_executed_contracts(session: AsyncSession = Depends(db_connect.session_dependency)):
    result = await select_not_executed_contracts(session=session)
    return result


@router.get("/deleted_contracts/")
async def get_deleted_contracts(session: AsyncSession = Depends(db_connect.session_dependency)):
    result = await select_deleted_contracts(session=session)
    return result


@router.get("storage/full-info")
async def get_storage_full_info(session: AsyncSession = Depends(db_connect.session_dependency)):
    result = await select_storage_items_with_products(session=session)
    return result


@router.get("/contracts/full-info")
async def get_contracts_full_info(session: AsyncSession = Depends(db_connect.session_dependency)):
    result = await select_full_contracts(session=session)
    return result

# @router.get("/contrs", response_model=Page[Any])
# async def get_filtered_contracts(page_params: Params = Depends(),
#                                  contract_filter: ContractFilter = FilterDepends(ContractFilter),
#                                  session: AsyncSession = Depends(db_connect.session_dependency)):
#     result = await select_filtered_contracts(filter=contract_filter,
#                                              session=session)
#     return paginate(result, page_params)
