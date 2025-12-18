import aiohttp
from bot.config import API_URL


async def telegram_auth(telegram_id: int, username: str | None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_URL}/auth/telegram/",
            json={
                "telegram_id": telegram_id,
                "username": username,
            }
        ) as response:

            if response.status != 200:
                text = await response.text()
                raise RuntimeError(f"Backend error {response.status}: {text}")

            data = await response.json()
            return data


async def refresh_access_token(refresh_token: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_URL}/auth/refresh/",
            json={"refresh": refresh_token}
        ) as response:
            if response.status != 200:
                text = await response.text()
                raise RuntimeError(f"Backend error {response.status}: {text}")
            return await response.json()


async def create_category(token: str, name: str):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"name": name}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_URL}/categories/",
            json=payload,
            headers=headers
        ) as response:
            if response.status != 201:
                raise RuntimeError(await response.text())
            return await response.json()


async def get_categories(token: str):
    headers = {"Authorization": f"Bearer {token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{API_URL}/categories/",
            headers=headers
        ) as response:
            return await response.json()


async def get_tasks(token: str):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/tasks/", headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                raise RuntimeError(
                    f"Backend error {response.status}: {text}"
                )

            return await response.json()  
        

async def create_task(token: str, title: str, due_date: str, categories: list[int], description: str = ""):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "title": title,
        "due_date": due_date,
        "categories": categories,
        "description": description,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/tasks/", headers=headers, json=payload) as response:
            if response.status != 201:
                text = await response.text()
                raise RuntimeError(f"Backend error {response.status}: {text}")
            return await response.json()