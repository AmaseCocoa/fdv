import os

from async_lru import alru_cache
from atproto import AsyncClient

from ..libs import env

env.load()

@alru_cache
async def get_profile(handle: str):
    client = AsyncClient()
    await client.login(os.getenv("ATPROTO_HANDLE"), os.getenv("ATPROTO_PASS"))
    return await client.get_profile(handle)
