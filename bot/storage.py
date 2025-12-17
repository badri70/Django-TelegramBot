import asyncio
import redis.asyncio as redis
from bot.config import REDIS_DB, REDIS_HOST, REDIS_PORT



redis_client: redis.Redis | None = None

async def get_redis() -> redis.Redis:
    global redis_client
    if not redis_client:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    return redis_client


async def save_token(telegram_id: int, token: str):
    r = await get_redis()
    await r.set(f"tg:{telegram_id}:token", token)

async def get_token(telegram_id: int) -> str | None:
    r = await get_redis()
    token = await r.get(f"tg:{telegram_id}:token")
    return token
