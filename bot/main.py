import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from bot.config import BOT_TOKEN
from bot.dialogs.add_task import add_task_dialog
from bot.handlers.tasks import router as tasks_router
from bot.handlers.start import router as start_router


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(tasks_router)
    dp.include_router(add_task_dialog)

    setup_dialogs(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
