import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from src.contract.algorithms import contract_rpe_map
from src.contract.crud import select_contract_by_id
from src.contract.schemas import ContractCreate
from src.database.models import Contract, Specification
from src.specification.crud import select_specifications_by_contract_id
from src.specification.schemas import SpecificationCreate
from src.view.view_query import select_contract_by_id_with_specifications, select_storage_item_by_product_id


async def insert_contract_with_specifications(session: AsyncSession,
                                              contract_in: ContractCreate,
                                              specifications_in: list[SpecificationCreate]) -> Contract:
    contract = Contract(**contract_in.model_dump())

    specifications = []
    for spec in specifications_in:
        specifications.append(Specification(**spec.model_dump()))

    session.add(contract)
    session.add_all(specifications)

    await session.commit()
    await session.refresh(contract)
    return contract


async def insert_specifications_for_new_contract(session: AsyncSession,
                                                 specifications_in: list[SpecificationCreate]):
    specifications = []
    for spec in specifications_in:
        specifications.append(Specification(**spec.model_dump()))
    session.add_all(specifications)
    await session.commit()
    contract_with_spec = await select_contract_by_id_with_specifications(session=session,
                                                                         contract_id=specifications_in[0].contract_id)
    return contract_with_spec


async def reserve_products_by_contract_id(session: AsyncSession, contract_id: int):
    contract = await select_contract_by_id(session=session, contract_id=contract_id)
    if contract.contract_type == 'income':
        return {'status': 200, 'result': 'Not implemented'}
    if contract.payment:
        return {'status': 200, 'result': 'Can not change reserve status. Contract has already been payed.'}

    specifications = await select_specifications_by_contract_id(session=session, contract_id=contract.contract_id)
    if contract.reserved:
        contract.reserved = False
        for specification in specifications:
            storage_item = await select_storage_item_by_product_id(session=session, product_id=specification.product_id)
            storage_item.available += specification.quantity
    else:
        contract.reserved = True
        for specification in specifications:
            storage_item = await select_storage_item_by_product_id(session=session, product_id=specification.product_id)
            storage_item.available -= specification.quantity
    await session.commit()
    await session.close()


async def payment_registration_by_contract_id(session: AsyncSession, contract_id: int):
    contract = await select_contract_by_id(session=session, contract_id=contract_id)
    specifications = await select_specifications_by_contract_id(session=session, contract_id=contract_id)

    if contract.contract_type == 'income':
        if contract_rpe_map(contract) == '110':
            contract.reserved = False
            contract.payment = False
            for specification in specifications:
                storage_item = await select_storage_item_by_product_id(session=session,
                                                                       product_id=specification.product_id)
                storage_item.available -= specification.quantity
                storage_item.owned -= specification.quantity
        elif contract_rpe_map(contract) == '000':

            contract.reserved = True
            contract.payment = True
            for specification in specifications:
                storage_item = await select_storage_item_by_product_id(session=session,
                                                                       product_id=specification.product_id)
                storage_item.available += specification.quantity
                storage_item.owned += specification.quantity

    if contract.contract_type == 'outcome':
        if contract_rpe_map(contract) in ('100', '110'):
            if contract.payment:
                contract.payment = False
                for specification in specifications:
                    storage_item = await select_storage_item_by_product_id(session=session,
                                                                           product_id=specification.product_id)
                    storage_item.owned += specification.quantity
            else:
                contract.payment = True
                for specification in specifications:
                    storage_item = await select_storage_item_by_product_id(session=session,
                                                                           product_id=specification.product_id)
                    storage_item.owned -= specification.quantity
    await session.commit()
    await session.close()


async def contract_execution_by_contract_id(session: AsyncSession, contract_id: int):
    contract = await select_contract_by_id(session=session, contract_id=contract_id)
    specifications = await select_specifications_by_contract_id(session=session, contract_id=contract_id)
    print(contract_rpe_map(contract))
    if contract_rpe_map(contract) not in ('110', '111'):
        return {'status': 200, 'result': 'Execution not available'}

    if contract.contract_type == 'income':
        if contract.executed:
            contract.executed = False
            for specification in specifications:
                storage_item = await select_storage_item_by_product_id(session=session,
                                                                       product_id=specification.product_id)
                storage_item.stored -= specification.quantity
            contract.executed_at = None
        else:
            contract.executed = True
            for specification in specifications:
                storage_item = await select_storage_item_by_product_id(session=session,
                                                                       product_id=specification.product_id)
                storage_item.stored += specification.quantity
            contract.executed_at = datetime.datetime.now()
    if contract.contract_type == 'outcome':
        if contract.executed:
            contract.executed = False
            for specification in specifications:
                storage_item = await select_storage_item_by_product_id(session=session,
                                                                       product_id=specification.product_id)
                storage_item.stored += specification.quantity
            contract.executed_at = None
        else:
            contract.executed = True
            for specification in specifications:
                storage_item = await select_storage_item_by_product_id(session=session,
                                                                       product_id=specification.product_id)
                storage_item.stored -= specification.quantity
            contract.executed_at = datetime.datetime.now()
    await session.commit()
    await session.close()


async def delete_contract(session: AsyncSession, contract_id: int):
    contract = await select_contract_by_id(session=session, contract_id=contract_id)
    contract.deleted_at = datetime.datetime.utcnow()
    await session.commit()
