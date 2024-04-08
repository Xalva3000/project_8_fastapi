from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.product.router import router as router_product
from src.contractor.router import router as router_contractor
from src.contract.router import router as router_contract
from src.execution.execution import router as router_execution
from src.specification.router import router as router_specification
from src.storage.router import router as router_storage
from src.view.view import router as router_view
from frontend.pages.router import router as router_pages
from starlette.staticfiles import StaticFiles

import uvicorn

app = FastAPI()

app.mount('/static', StaticFiles(directory='frontend/static'), name='static')

app.include_router(router=router_product, prefix='/products')
app.include_router(router=router_contractor, prefix='/contractors')
app.include_router(router=router_contract, prefix='/contracts')
app.include_router(router=router_specification, prefix='/specification')
app.include_router(router=router_storage, prefix='/storage')
app.include_router(router=router_execution, prefix='/execution')
app.include_router(router=router_view, prefix='/view')
app.include_router(router=router_pages, prefix='/pages')
add_pagination(app)

# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url(
#         "redis://localhost", encoding="utf-8", decode_responses=True
#     )
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
