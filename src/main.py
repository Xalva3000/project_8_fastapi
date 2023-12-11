from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from src.database.connect import DBConnect
from src.product.router import router as router_product
from src.contractor.router import router as router_contractor
from src.contract.router import router as router_contract
from src.contract.execution import router as router_execution
from src.specification.router import router as router_specification
from src.possession.router import router as router_possession
from src.storage.router import router as router_storage

import uvicorn

app = FastAPI()

app.include_router(router=router_product, prefix='/products')
app.include_router(router=router_contractor, prefix='/contractors')
app.include_router(router=router_contract, prefix='/contracts')
app.include_router(router=router_specification, prefix='/specification')
app.include_router(router=router_possession, prefix='/possession')
app.include_router(router=router_storage, prefix='/storage')
app.include_router(router=router_execution, prefix='/execution')

# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url(
#         "redis://localhost", encoding="utf-8", decode_responses=True
#     )
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
