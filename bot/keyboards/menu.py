from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/tasks")],
        [KeyboardButton(text="/add_task")],
    ],
    resize_keyboard=True
)
