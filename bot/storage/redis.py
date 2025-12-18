import redis.asyncio as redis
from bot.config import REDIS_DB, REDIS_HOST, REDIS_PORT

redis_client: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    global redis_client
    if not redis_client:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )
    return redis_client

async def save_tokens(
    telegram_id: int,
    access_token: str,
    refresh_token: str
):
    r = await get_redis()
    await r.set(f"tg:{telegram_id}:access", access_token)
    await r.set(f"tg:{telegram_id}:refresh", refresh_token)


async def get_access_token(telegram_id: int) -> str | None:
    r = await get_redis()
    return await r.get(f"tg:{telegram_id}:access")


async def get_refresh_token(telegram_id: int) -> str | None:
    r = await get_redis()
    return await r.get(f"tg:{telegram_id}:refresh")


async def save_access_token(telegram_id: int, access_token: str):
    r = await get_redis()
    await r.set(f"tg:{telegram_id}:access", access_token)
    

async def get_tokens(telegram_id: int) -> dict | None:
    r = await get_redis()
    access = await r.get(f"tg:{telegram_id}:access")
    refresh = await r.get(f"tg:{telegram_id}:refresh")
    if access and refresh:
        return {"access": access, "refresh": refresh}
    return None