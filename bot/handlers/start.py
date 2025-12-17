from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

# from bot.api.todo_api import telegram_auth
# from bot.storage import save_token

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    tg_id = message.from_user.id
    username = message.from_user.username

    # response = await telegram_auth(tg_id, username)
    # save_token(tg_id, response["access"])

    # if response["created"]:
    #     await message.answer("👋 Добро пожаловать! Вы успешно зарегистрированы.")
    # else:
    #     await message.answer("👋 С возвращением!")

    await message.answer("Используйте /tasks или /add_task")
