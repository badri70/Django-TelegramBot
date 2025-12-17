import aiohttp
from bot.config import API_URL


async def telegram_auth(telegram_id: int, username: str | None):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_URL}/auth/telegram/",
            json={
                "telegram_id": telegram_id,
                "username": username,
            }
        ) as response:
            return await response.json()


async def get_tasks(token: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{API_URL}/tasks/",
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            return await response.json()


async def create_task(token: str, title: str, category_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_URL}/tasks/",
            json={
                "title": title,
                "category": category_id
            },
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            return await response.json()