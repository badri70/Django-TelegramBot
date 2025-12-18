from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.api.todo_api import telegram_auth
from bot.storage.redis import save_tokens  

router = Router()

from bot.storage.redis import save_tokens

@router.message(Command("start"))
async def start_handler(message: Message):
    tg_id = message.from_user.id
    username = message.from_user.username

    response = await telegram_auth(tg_id, username)
    
    await save_tokens(tg_id, response["access"], response["refresh"])

    if response.get("created"):
        await message.answer("👋 Добро пожаловать! Вы успешно зарегистрированы.")
    else:
        await message.answer("👋 С возвращением!")
        
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/tasks"), KeyboardButton(text="/add_task")],
            [KeyboardButton(text="/categories"), KeyboardButton(text="/add_category")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        text="Привет! Выбери одну из команд ниже:",
        reply_markup=keyboard
    )    