from aiogram.fsm.state import StatesGroup, State


class AddTaskSG(StatesGroup):
    title = State()
    category = State()


from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput
from bot.api.todo_api import create_task


async def title_handler(message, widget, manager: DialogManager, text: str):
    manager.dialog_data["title"] = text
    await manager.next()


async def category_handler(message, widget, manager: DialogManager, text: str):
    title = manager.dialog_data["title"]
    category_id = int(text)

    token = "USER_JWT_TOKEN"  # обычно хранится в БД
    await create_task(token, title, category_id)

    await message.answer("✅ Задача успешно добавлена")
    await manager.done()


add_task_dialog = Dialog(
    Window(
        Const("✏️ Введите название задачи"),
        TextInput(id="title", on_success=title_handler),
        state=AddTaskSG.title,
    ),
    Window(
        Const("📂 Введите ID категории"),
        TextInput(id="category", on_success=category_handler),
        state=AddTaskSG.category,
    ),
)
