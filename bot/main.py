import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from bot.config import BOT_TOKEN
from bot.dialogs.add_task import add_task_dialog
from bot.dialogs.add_category import add_category_dialog
from bot.handlers.tasks import router as tasks_router
from bot.handlers.start import router as start_router
from bot.handlers.categories import router as categories_router
from bot.notify_service import start_notify_server

async def start_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(tasks_router)
    dp.include_router(categories_router)
    dp.include_router(add_category_dialog)
    dp.include_router(add_task_dialog)

    setup_dialogs(dp)
    await dp.start_polling(bot)

async def main():
    await asyncio.gather(
        start_bot(),
        start_notify_server()
    )

if __name__ == "__main__":
    import sys, asyncio
    if sys.platform == "darwin":
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())
