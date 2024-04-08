from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.contract.crud import mark_contract_as_deleted
from src.contract.dependencies import contract_by_id
from src.database.connect import db_connect
from src.database.models import Contract
from src.execution.execution_query import payment_registration_by_contract_id, contract_execution_by_contract_id
from src.product.crud import select_all_products
from src.storage.crud import select_all_storage_items, insert_storage_item
from src.storage.schemas import StorageItemCreate

router = APIRouter(tags=['Execution'])


@router.post("/{contract_id}/reserve")
async def reserve_products_by_contract_id(contract_id: int,
                                          session: AsyncSession = Depends(db_connect.session_dependency)):
    result = await reserve_products_by_contract_id(session=session, contract_id=contract_id)
    return result


@router.post("/{contract_id}/payment")
async def register_payment_of_products_by_contract_id(contract_id: int,
                                                      session: AsyncSession = Depends(db_connect.session_dependency)):
    result = await payment_registration_by_contract_id(session=session, contract_id=contract_id)
    return result


@router.post("/{contract_id}/execution")
async def confirm_execution(contract_id: int,
                            session: AsyncSession = Depends(db_connect.session_dependency)):
    result = await contract_execution_by_contract_id(session=session, contract_id=contract_id)
    return result


@router.patch("/refresh-storage/")
async def refresh_storage(session: AsyncSession = Depends(db_connect.session_dependency)):
    all_products = await select_all_products(session=session)
    storage_list = await select_all_storage_items(session=session)
    storage_ids = [stor.product_id for stor in storage_list]
    for product in all_products:
        if product.product_id not in storage_ids:
            storage_item_in = StorageItemCreate(product_id=product.product_id)
            await insert_storage_item(session=session, storage_item_in=storage_item_in)
    result = await select_all_storage_items(session=session)
    return result


@router.post("/delete_contract/{contract_id}")
async def delete_contract_with_specifications(session: AsyncSession = Depends(db_connect.session_dependency),
                                              contract: Contract = Depends(contract_by_id)):
    await mark_contract_as_deleted(session=session, contract=contract)
