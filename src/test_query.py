import asyncio
from src.operations.router import get_specific
from auth.database import get_async_session

async def main():
    result = await get_specific('first', get_async_session())
    print(result)


if __name__ == '__main__':
    asyncio.run(main())