# bot/notify_service.py
from aiohttp import web
from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.config import BOT_TOKEN


async def notify(request):
    data = await request.json()
    tg_id = data.get("telegram_id")
    task_title = data.get("task_title")
    task_id = data.get("task_id")

    if not tg_id or not task_title or not task_id:
        return web.json_response({"error": "telegram_id, task_title and task_id required"}, status=400)

    bot = Bot(token=BOT_TOKEN)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Завершить задачу",
                    callback_data=f"complete_task:{task_id}"
                )
            ]
        ]
    )

    try:
        await bot.send_message(
            chat_id=tg_id,
            text=f"🕒 Срок задачи наступил: {task_title}",
            reply_markup=keyboard
        )
        await bot.session.close()
        return web.json_response({"status": "ok"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


async def start_notify_server():
    app = web.Application()
    app.add_routes([web.post("/notify", notify)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8001)
    await site.start()
    print("Notify service started at http://0.0.0.0:8001")
