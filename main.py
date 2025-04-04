import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv
from content import content

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

# Для хранения прогресса пользователя
user_progress = {}

def get_next_content(user_id):
    index = user_progress.get(user_id, 0)
    if index >= len(content):
        return None
    item = content[index]
    user_progress[user_id] = index + 1
    return item

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_progress[message.from_user.id] = 0
    await send_next(message.chat.id, message.from_user.id)

@dp.callback_query_handler(lambda c: c.data == "next")
async def next_handler(callback_query: types.CallbackQuery):
    await send_next(callback_query.message.chat.id, callback_query.from_user.id)
    await callback_query.answer()

async def send_next(chat_id, user_id):
    item = get_next_content(user_id)
    if item is None:
        await bot.send_message(chat_id, "Конец контента.")
        return

    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("Дальше ▶️", callback_data="next"))

    if item["type"] == "text":
        await bot.send_message(chat_id, item["data"], reply_markup=keyboard)
    elif item["type"] == "video":
        await bot.send_video(chat_id, item["data"], reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp)
