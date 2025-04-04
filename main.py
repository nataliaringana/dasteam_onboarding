import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from content import content
from aiogram.client.default import DefaultBotProperties

load_dotenv()
bot = Bot(
    token=os.getenv("BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Храним прогресс по пользователям
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

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
