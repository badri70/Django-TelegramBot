from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const
from aiogram.fsm.state import StatesGroup, State

from bot.api.todo_api import create_category
from bot.storage.token_manager import get_valid_token


class AddCategorySG(StatesGroup):
    title = State()


async def on_category_entered(message, widget, manager: DialogManager, value: str):
    tg_id = message.from_user.id
    token = await get_valid_token(tg_id)

    await create_category(token, value)

    await message.answer("✅ Категория добавлена")
    await manager.done()


add_category_dialog = Dialog(
    Window(
        Const("📂 Введите название категории:"),
        TextInput(
            id="category_title",
            on_success=on_category_entered
        ),
        state=AddCategorySG.title
    )
)
