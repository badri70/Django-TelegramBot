from aiogram import Router
from aiogram.types import Message
from bot.api.todo_api import get_tasks
from aiogram.filters import Command


router = Router()


@router.message(Command("tasks"))
async def tasks_list(message: Message):
    token = "USER_JWT_TOKEN"

    tasks = await get_tasks(token)
    if not tasks:
        await message.answer("📭 У вас нет задач")
        return

    text = "📝 Ваши задачи:\n\n"
    for task in tasks:
        text += (
            f"• {task['title']}\n"
            f"  📂 {task['category']['name'] if task['category'] else 'Без категории'}\n"
            f"  📅 {task['created_at'][:10]}\n\n"
        )

    await message.answer(text)