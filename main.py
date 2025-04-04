import os
import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from aiohttp import web
from dotenv import load_dotenv

from content import content

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") + WEBHOOK_PATH  # полный адрес: https://your-render-app.onrender.com/webhook/<token>

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

user_progress = {}

def get_next_content(user_id):
    index = user_progress.get(user_id, 0)
    if index >= len(content):
        return None
    item = content[index]
    user_progress[user_id] = index + 1
    return item

@dp.message(CommandStart())
async def start(message: types.Message):
    user_progress[message.from_user.id] = 0
    await send_next(message.chat.id, message.from_user.id)

@dp.callback_query(F.data == "next")
async def next_handler(callback: types.CallbackQuery):
    await send_next(callback.message.chat.id, callback.from_user.id)
    await callback.answer()

async def send_next(chat_id, user_id):
    item = get_next_content(user_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Дальше ▶️", callback_data="next")]]
    )

    if item is None:
        await bot.send_message(chat_id, "📦 Конец контента.")
    elif item["type"] == "text":
        await bot.send_message(chat_id, item["data"], reply_markup=keyboard)
    elif item["type"] == "video":
        await bot.send_video(chat_id, item["data"], reply_markup=keyboard)

# Создаём веб-приложение для Render
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()

async def main():
    app = web.Application()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Вешаем хендлер
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)

    setup_application(app, dp)
    port = int(os.environ.get("PORT", 8080))
    return app

if __name__ == "__main__":
    web.run_app(main(), port=int(os.environ.get("PORT", 8080)))
