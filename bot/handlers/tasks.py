from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager
from aiogram.types import CallbackQuery
import requests
from bot.api.todo_api import get_tasks
from bot.storage.token_manager import get_valid_token
from bot.dialogs.add_task import AddTaskSG
from bot.config import API_URL
import aiohttp

router = Router()

@router.message(Command("tasks"))
async def tasks_list(message: Message):
    tg_id = message.from_user.id
    token = await get_valid_token(tg_id)

    tasks = await get_tasks(token)

    if not tasks:
        await message.answer("У тебя пока нет задач")
        return

    text = "📝 Твои задачи:\n\n"
    for task in tasks:
        categories = ", ".join(cat["name"] for cat in task.get("categories", []))
        text += (
            f"• {task['title']}\n"
            f"  📂 {categories or 'Без категории'}\n"
            f"  🕒 {task['created_at']}\n\n"
        )

    await message.answer(text)


@router.message(Command("add_task"))
async def add_task(message, dialog_manager: DialogManager):
    await dialog_manager.start(AddTaskSG.title)
    

@router.callback_query(lambda c: c.data and c.data.startswith("complete_task:"))
async def complete_task_callback(query: CallbackQuery):
    task_id = query.data.split(":")[1]
    tg_id = query.from_user.id

    token = await get_valid_token(tg_id)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{API_URL}/tasks/{task_id}/complete/", headers=headers) as resp:
            if resp.status == 200:
                await query.message.edit_text("✅ Задача завершена!")
            else:
                text = await resp.text()
                await query.message.edit_text(f"❌ Не удалось завершить задачу: {text}")