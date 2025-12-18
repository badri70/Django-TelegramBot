from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager
from bot.api.todo_api import get_categories
from bot.storage.token_manager import get_valid_token
from bot.dialogs.add_category import AddCategorySG

router = Router()


@router.message(Command("add_category"))
async def add_category(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AddCategorySG.title)


@router.message(Command("categories"))
async def categories_list(message: Message):
    tg_id = message.from_user.id

    try:
        token = await get_valid_token(tg_id)
    except RuntimeError:
        await message.answer("❌ Вы не авторизованы. Используйте /start")
        return

    response = await get_categories(token)
    categories = response if isinstance(response, list) else []

    if not categories:
        await message.answer("📂 У вас пока нет категорий")
        return

    text = "📂 *Ваши категории:*\n\n"
    for cat in categories:
        # убедимся, что cat — словарь
        if isinstance(cat, dict):
            text += f"• {cat.get('id', '—')} — {cat.get('name', 'Без названия')}\n"

    await message.answer(text, parse_mode="Markdown")
