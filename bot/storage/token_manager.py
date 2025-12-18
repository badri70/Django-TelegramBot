from bot.storage.redis import get_tokens, save_tokens
from bot.api.todo_api import refresh_access_token

async def get_valid_token(telegram_id: int) -> str:
    tokens = await get_tokens(telegram_id)
    if not tokens:
        raise RuntimeError("User not authorized. Используйте /start")

    access = tokens.get("access")
    refresh = tokens.get("refresh")

    try:
        return access
    except RuntimeError:
        new_tokens = await refresh_access_token(refresh)
        await save_tokens(
            telegram_id,
            access_token=new_tokens["access"],
            refresh_token=new_tokens["refresh"]
        )
        return new_tokens["access"]
