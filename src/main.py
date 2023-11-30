from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from src.product.router import router as router_product
from src.contractor.router import router as router_contractor
from src.database.connect import DBConnect
import uvicorn

app = FastAPI()

app.include_router(router=router_contractor, prefix='/contractors')
app.include_router(router=router_product, prefix='/products')

# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url(
#         "redis://localhost", encoding="utf-8", decode_responses=True
#     )
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
