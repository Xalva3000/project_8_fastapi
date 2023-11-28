from fastapi_users import FastAPIUsers

from src.auth.auth import auth_backend
from src.auth.database import ApiUser
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from fastapi import FastAPI, Depends
from src.operations.router import router as router_operation
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from src.producer.router import router as router_producer

from redis import asyncio as aioredis


app = FastAPI(title="Trading App", tags=["items"])


fastapi_users = FastAPIUsers[ApiUser, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(router_operation)
app.include_router(router_producer)

current_user = fastapi_users.current_user()


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/protected-route")
def protected_route(user: ApiUser = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/unprotected-route")
def protected_route():
    return f"Hello, anonym"


# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
#     return {"q": q, "skip": skip, "limit": limit}
#
#
# @app.get("/items/")
# async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons
#
#
# @app.get("/users/")
# async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons


# @app.get('/names/{user_id}', response_model=List[int])
# def get_user_name(user_id: int):
#     result = SyncQuery.get_user(user_id)
#     return result
#
#
# @app.get('/limited_ids/{lst}')
# def get_ids_in_range(lower_limit: int = 5*10**6, upper_limit: int = 6*10**6):
#     all_ids = SyncQuery.get_all_users()
#     return [user.user_id for user in filter(lambda user: user.user_id in range(lower_limit, upper_limit + 1), all_ids)]
#
#
# @app.post('/users/')
# def update_user_info(users: List[UserInfo]):
#     lst_temp = []
#     for user in users:
#         lst_temp.append(user.user_id)
#         SyncQuery.update_user_info(user)
#     return {'status': 200, 'data': f"users {lst_temp} updated"}
#
#
# @app.post('/users/{user_id}')
# def update_current_page(user_id: int, new_page: int):
#     SyncQuery.update_user_current_page(user_id, new_page)
#     user = SyncQuery.get_user(user_id)
#     return {'status': 200, 'data': user}


# def main():
# if __name__ == '__main__':
# main()
