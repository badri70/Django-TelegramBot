from datetime import datetime
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const
from aiogram.fsm.state import StatesGroup, State
from bot.api.todo_api import create_task
from bot.storage.token_manager import get_valid_token

class AddTaskSG(StatesGroup):
    title = State()
    categories = State()
    description = State()
    due_date = State()


async def on_task_title_entered(message, widget, manager: DialogManager, value: str):
    manager.current_context().dialog_data["title"] = value
    await manager.next()


async def on_categories_entered(message, widget, manager: DialogManager, value: str):
    """
    Пользователь вводит ID категорий через запятую: 1,2,3
    """
    try:
        categories = [int(cat_id.strip()) for cat_id in value.split(",")]
    except ValueError:
        await message.answer("❌ Введите категории числовыми ID через запятую, например: 1,2,3")
        return
    manager.current_context().dialog_data["categories"] = categories
    await manager.next()


async def on_description_entered(message, widget, manager: DialogManager, value: str):
    manager.current_context().dialog_data["description"] = value
    await manager.next()


async def on_due_date_entered(message, widget, manager: DialogManager, value: str):
    try:
        due_date = datetime.strptime(value, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.answer("❌ Введите дату в формате YYYY-MM-DD HH:MM")
        return

    data = manager.current_context().dialog_data
    tg_id = message.from_user.id
    token = await get_valid_token(tg_id)

    await create_task(
        token=token,
        title=data["title"],
        description=data["description"],
        due_date=due_date.isoformat(),
        categories=data["categories"]
    )

    await message.answer("✅ Задача создана!")
    await manager.done()


add_task_dialog = Dialog(
    Window(
        Const("📝 Введите название задачи:"),
        TextInput(id="task_title", on_success=on_task_title_entered),
        state=AddTaskSG.title
    ),
    Window(
        Const("📂 Введите категории задачи (ID через запятую, например: 1,2,3):"),
        TextInput(id="task_categories", on_success=on_categories_entered),
        state=AddTaskSG.categories
    ),
    Window(
        Const("✏️ Введите описание задачи:"),
        TextInput(id="task_description", on_success=on_description_entered),
        state=AddTaskSG.description
    ),
    Window(
        Const("📅 Введите дату выполнения задачи (YYYY-MM-DD HH:MM):"),
        TextInput(id="task_due_date", on_success=on_due_date_entered),
        state=AddTaskSG.due_date
    )
)
