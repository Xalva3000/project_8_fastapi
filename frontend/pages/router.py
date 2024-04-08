from datetime import datetime, date
from urllib.parse import urlparse

from fastapi import APIRouter, Request, Form
from fastapi.params import Depends
from fastapi.templating import Jinja2Templates
from fastapi_pagination import paginate, Params

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import _TemplateResponse

from frontend.pages.schemas import ExecutionForm
from src.contract.schemas import ContractCreate
from src.contractor.crud import select_contractor_by_id, update_contractor, insert_contractor
from src.contractor.schemas import ContractorUpdatePartial
from src.database.connect import db_connect
from src.database.models import Product, Contractor
from src.database.models import StorageItem
from src.view.view import get_storage_full_info
from src.execution.execution_query import insert_specifications_for_new_contract, \
    reserve_products_by_contract_id, payment_registration_by_contract_id, contract_execution_by_contract_id, \
    delete_contract
from src.product.crud import insert_product, update_product, select_product_by_id
from src.product.router import get_all_products
from src.contractor.router import get_all_contractors
from src.product.schemas import ProductCreate, ProductUpdatePartial
from src.contractor.schemas import ContractorCreate
from src.specification.schemas import SpecificationCreate
from src.contract.crud import insert_contract
from src.view.view_scheme import ContractFilter, ContractForm, PageForm

from src.view.view_query import select_today_contracts, select_outcome_contracts, select_income_contracts, \
    select_no_execution_contracts, select_nonzero_storage_items_with_products, \
    select_free_to_sell_storage_items_with_products, select_owned_storage_items_with_products, \
    select_stored_storage_items_with_products, select_storage_items_with_products, \
    select_deleted_contracts, select_full_contracts, select_contracts_on_date, select_full_contract_by_id, \
    select_filtered_contracts, select_contracts_by_idlist

router = APIRouter(tags=['pages'])

templates_directories = ["frontend/templates",
                         "frontend/templates/menu",
                         "frontend/templates/product",
                         "frontend/templates/contract",
                         "frontend/templates/contractor",
                         "frontend/templates/storage",
                         ]

COMMANDS = {"reserve": reserve_products_by_contract_id,
            "payment": payment_registration_by_contract_id,
            "execution": contract_execution_by_contract_id,
            "delete": delete_contract, }

VIEW_RESULT = {"all": select_full_contracts,
               "outcome": select_outcome_contracts,
               "income": select_income_contracts,
               "today": select_today_contracts,
               "no_execution": select_no_execution_contracts,
               "deleted": select_deleted_contracts,
               "on_date": select_contracts_on_date,
               }


def get_current_date():
    return datetime.utcnow().date()


templates = Jinja2Templates(directory=templates_directories)


# static = Jinja2Templates(directory="frontend/static")

@router.get("/menu")
async def get_main_menu_page(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})


@router.post("/contracts/on_date")
async def get_contracts_on_date_page(request: Request,
                                     session: AsyncSession = Depends(db_connect.session_dependency),
                                     day: str = Form(...)):
    contracts_on_date = await select_contracts_on_date(session=session, user_date=day)
    return templates.TemplateResponse("contracts.html", {"request": request,
                                                         "subtitle": f"on_date_{day}",
                                                         "current_date": day,
                                                         "contracts": contracts_on_date})


@router.post("/contracts/by_contract_id/{contract_id}")
async def get_contracts_on_date_page(request: Request,
                                     contract_id: int,
                                     session: AsyncSession = Depends(db_connect.session_dependency),
                                     ):
    contracts = await select_full_contract_by_id(session=session, contract_id=contract_id)
    return templates.TemplateResponse("contracts.html", {"request": request,
                                                         "subtitle": f"by_contract_id_{contract_id}",
                                                         "contracts": contracts})


@router.get("/contracts/filter/")
async def get_contracts_filtered_page(request: Request,
                                      session: AsyncSession = Depends(db_connect.session_dependency),
                                      current_date: date = Depends(get_current_date)):
    # if demand:
    #     command, contract_id = demand.split('=')
    #     await COMMANDS[command](session=session, contract_id=int(contract_id))

    form = await request.form()
    execution_form = ExecutionForm(**form)
    contract_form = ContractForm(**form)
    print(contract_form.__dict__)
    page_form = PageForm(**form)
    filter = ContractFilter(**contract_form.__dict__)
    print(filter.__dict__)
    page_params = Params(**page_form.__dict__)

    contract_ids = await select_filtered_contracts(filter=filter, session=session)
    page = paginate(contract_ids, page_params)
    contracts = await select_contracts_by_idlist(session=session, id_list=page.items)

    return templates.TemplateResponse("contracts_filter.html", {"request": request,
                                                                "filter_params": filter,
                                                                "page_params": page,
                                                                "contracts": contracts})


@router.post("/contracts/filter/")
async def get_contracts_filtered_page(request: Request,
                                      session: AsyncSession = Depends(db_connect.session_dependency),
                                      current_date: date = Depends(get_current_date)):
    form = await request.form()
    print(form)
    execution_form = ExecutionForm(**form)

    if execution_form.model_dump(exclude_unset=True):
        command, contract_id = execution_form.get_demand()
        await COMMANDS[command](session=session, contract_id=contract_id)

    contract_form = ContractForm(**form)
    print(contract_form.__dict__)
    page_form = PageForm(**form)
    filter = ContractFilter(**contract_form.__dict__)
    print(filter.__dict__)

    page_params = Params(**page_form.__dict__)

    contract_ids = await select_filtered_contracts(filter=filter, session=session)
    page = paginate(contract_ids, page_params)
    contracts = await select_contracts_by_idlist(session=session, id_list=page.items)

    return templates.TemplateResponse("contracts_filter.html", {"request": request,
                                                                "filter_params": filter,
                                                                "page_params": page,
                                                                "contracts": contracts})


# @router.get("/contracts/{subtitle}")
# async def get_contracts_page(request: Request,
#                              subtitle: str,
#                              current_date: date = Depends(get_current_date)):
#     demand = urlparse(str(request.url)).query
#     async with db_connect.session_factory() as session:
#         if demand:
#             command, contract_id = demand.split('=')
#             await COMMANDS[command](session=session, contract_id=int(contract_id))
#         # if "on_date" in subtitle:
#         #     result = await select_contracts_on_date(session=session,
#         #                                             user_date=subtitle.removeprefix("on_date_"))
#         # else:
#         result = await VIEW_RESULT[subtitle](session=session)
#     return templates.TemplateResponse("contracts.html", {"request": request,
#                                                          "subtitle": subtitle,
#                                                          "current_date": current_date,
#                                                          "contracts": result})


@router.get("/add_contract/")
async def get_contract_form_page(request: Request, spec_num: str,
                                 session: AsyncSession = Depends(db_connect.session_dependency)):
    contractors = await get_all_contractors(session=session)
    storage_items = await select_storage_items_with_products(session=session)
    return templates.TemplateResponse("add_contract.html",
                                      {"request": request,
                                       "spec_num": int(spec_num),
                                       "storage_items": storage_items,
                                       "contractors": contractors})


@router.post("/create_contract_with_specifications/")
async def create_contract_with_specifications(request: Request,
                                              session: AsyncSession = Depends(db_connect.session_dependency)):
    form_data = await request.form()
    data = dict(form_data)
    print(data)
    contract_in = ContractCreate(**data)
    contract = await insert_contract(session=session, contract_in=contract_in)

    num_of_specifications = len(list(filter(lambda key: 'product' in key, data.keys())))
    specifications_in: list = []

    for i in range(num_of_specifications):
        specifications_in.append(SpecificationCreate(contract_id=contract.contract_id,
                                                     product_id=data['product' + str(i)],
                                                     quantity=data['quantity' + str(i)],
                                                     price=data['price' + str(i)]))
    registered_contract = await insert_specifications_for_new_contract(session=session,
                                                                       specifications_in=specifications_in)

    return templates.TemplateResponse("any_result.html", {"request": request, "result": registered_contract})


@router.get("/contracts/deleted")
async def get_deleted_contracts_page(request: Request,
                                     session: AsyncSession = Depends(db_connect.session_dependency)):
    result = await select_deleted_contracts(session=session)
    return templates.TemplateResponse("contracts.html", {"request": request, "contracts": result})


@router.get("/products")
async def get_products_page(request: Request,
                            products: list[Product] = Depends(get_all_products)):
    form = await request.form()
    print(form)
    if form:
        page_form = PageForm(**form)
        print(page_form)
    else:
        page_form = PageForm(page='1', size='20')
    page_params = Params(**page_form.__dict__)
    page_params = paginate(products, page_params)

    return templates.TemplateResponse("products.html", {"request": request,
                                                        "page_params": page_params,
                                                        "subtitle": "products",
                                                        "products": page_params.items})


@router.post("/products")
async def get_products_page(request: Request,
                            products: list[Product] = Depends(get_all_products)):
    form = await request.form()
    if form:
        page_form = PageForm(**form)
    else:
        page_form = PageForm(page='1', size='20')
    params = Params(**page_form.__dict__)
    page_params = paginate(products, params)

    return templates.TemplateResponse("products.html", {"request": request,
                                                        "page_params": page_params,
                                                        "subtitle": "products",
                                                        "products": page_params.items})


@router.get("/add_product/")
async def get_product_form_page(request: Request):
    return templates.TemplateResponse("add_product.html", {"request": request})


@router.post("/create_product/")
async def create_product(request: Request,
                         session: AsyncSession = Depends(db_connect.session_dependency)) -> _TemplateResponse:
    data = await request.form()
    product_in = ProductCreate(**dict(data))
    print(product_in)
    result = await insert_product(session=session, product_in=product_in)
    return templates.TemplateResponse("any_result.html", {"request": request, "results": [result]})


@router.get("/update_product/{product_id}")
async def get_update_product_form_page(request: Request,
                                       product_id: int,
                                       session: AsyncSession = Depends(db_connect.session_dependency)):
    old_product = await select_product_by_id(session=session, product_id=product_id)
    print(old_product)
    return templates.TemplateResponse("update_product.html", {"request": request,
                                                              "old_product": old_product})


@router.post("/update_product/submit/{product_id}")
async def update_product_submit_button(request: Request,
                                       product_id: int,
                                       session: AsyncSession = Depends(
                                           db_connect.session_dependency)) -> _TemplateResponse:
    data = await request.form()
    product_update = ProductUpdatePartial(**dict(data))
    product = await select_product_by_id(session=session, product_id=product_id)
    result = await update_product(session=session,
                                  product=product,
                                  product_update=product_update,
                                  partial=True)
    return templates.TemplateResponse("any_result.html", {"request": request, "results": result})


@router.get("/contractors")
async def get_contractors_page(request: Request,
                               contractors: list[Contractor] = Depends(get_all_contractors)):
    form = await request.form()
    if form:
        page_form = PageForm(**form)
    else:
        page_form = PageForm(page='1', size='20')
    params = Params(**page_form.__dict__)
    page_params = paginate(contractors, params)

    return templates.TemplateResponse("contractors.html", {"request": request,
                                                           "page_params": page_params,
                                                           "subtitle": "contractors",
                                                           "contractors": page_params.items})


@router.post("/contractors")
async def get_contractors_page(request: Request,
                               contractors: list[Contractor] = Depends(get_all_contractors)):
    form = await request.form()
    if form:
        page_form = PageForm(**form)
    else:
        page_form = PageForm(page='1', size='20')
    params = Params(**page_form.__dict__)
    page_params = paginate(contractors, params)

    return templates.TemplateResponse("contractors.html", {"request": request,
                                                           "page_params": page_params,
                                                           "subtitle": "contractors",
                                                           "contractors": page_params.items})


@router.get("/add_contractor/")
async def get_contractor_form_page(request: Request):
    return templates.TemplateResponse("add_contractor.html", {"request": request})


@router.post("/create_contractor/")
async def create_contractor(request: Request,
                            session: AsyncSession = Depends(db_connect.session_dependency)) -> _TemplateResponse:
    data = await request.form()
    contractor_in = ContractorCreate(**dict(data))
    print(contractor_in)
    result = await insert_contractor(session=session, contractor_in=contractor_in)
    return templates.TemplateResponse("any_result.html", {"request": request, "results": [result]})


@router.get("/update_contractor/{contractor_id}")
async def get_update_product_form_page(request: Request,
                                       contractor_id: int,
                                       session: AsyncSession = Depends(db_connect.session_dependency)):
    old_contractor = await select_contractor_by_id(session=session, contractor_id=contractor_id)
    return templates.TemplateResponse("update_contractor.html", {"request": request,
                                                                 "old_contractor": old_contractor})


@router.post("/update_contractor/submit/{contractor_id}")
async def update_product_submit_button(request: Request,
                                       contractor_id: int,
                                       session: AsyncSession = Depends(
                                           db_connect.session_dependency)) -> _TemplateResponse:
    data = await request.form()
    contractor_update = ContractorUpdatePartial(**dict(data))
    contractor = await select_contractor_by_id(session=session, contractor_id=contractor_id)
    result = await update_contractor(session=session,
                                     contractor=contractor,
                                     contractor_update=contractor_update,
                                     partial=True)
    return templates.TemplateResponse("any_result.html", {"request": request, "results": result})


@router.get("/storage")
async def get_storage_page(request: Request, storage: list[StorageItem] = Depends(get_storage_full_info)):
    return templates.TemplateResponse("storage.html", {"request": request, "storage": storage})


@router.get("/storage/nonzero")
async def get_nonzero_storage_page(request: Request, session: AsyncSession = Depends(db_connect.session_dependency)):
    storage = await select_nonzero_storage_items_with_products(session=session)
    return templates.TemplateResponse("storage.html", {"request": request, "storage": storage})


@router.get("/storage/free_to_sell")
async def get_free_to_sell_storage_items_page(request: Request,
                                              session: AsyncSession = Depends(db_connect.session_dependency)):
    storage = await select_free_to_sell_storage_items_with_products(session=session)
    return templates.TemplateResponse("free_to_sell.html", {"request": request, "storage": storage})


@router.get("/storage/ownership")
async def get_owned_storage_items_page(request: Request,
                                       session: AsyncSession = Depends(db_connect.session_dependency)):
    storage = await select_owned_storage_items_with_products(session=session)
    return templates.TemplateResponse("ownership.html", {"request": request, "storage": storage})


@router.get("/storage/stored")
async def get_stored_storage_items_page(request: Request,
                                        session: AsyncSession = Depends(db_connect.session_dependency)):
    storage = await select_stored_storage_items_with_products(session=session)
    return templates.TemplateResponse("stored.html", {"request": request, "storage": storage})
