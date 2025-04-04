import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.filters import Command
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")  # Получаем токен из переменных окружения
bot = Bot(token=API_TOKEN)

# Новый способ создания Dispatcher в aiogram 3.x
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создаем Router для регистрации обработчиков
router = Router()

# Ссылка на видео с Google Drive
video_id = "1KlIj_WqsURqs7wKzuySAtfNZf1MzGSBe"  # Замените на свой ID видео
video_url = f"https://drive.google.com/uc?id={video_id}"

# Путь для сохранения видео локально
video_path = "video.mp4"

# Функция для скачивания видео с Google Drive
def download_video(url, path):
    response = requests.get(url, allow_redirects=True)
    with open(path, 'wb') as file:
        file.write(response.content)
    print(f"Видео скачано по пути: {path}")

# Текст для первого шага
step_1_text = """
Hallo liebe/r {Vorname}! 😊

🎉 HERZLICH WILLKOMMEN IM TEAM! 🎉
Ich freue mich, dich auf deinem Weg bei RINGANA zu begleiten. Gemeinsam schaffen wir Großes – mit Leichtigkeit und Freude.
"""

# Функция для отправки видео и текста
async def send_step(chat_id):
    # Отправляем текст
    await bot.send_message(chat_id, step_1_text.format(Vorname="User"))

    # Скачиваем видео
    download_video(video_url, video_path)

    # Отправляем видео
    with open(video_path, 'rb') as video:
        await bot.send_video(chat_id, video, caption="Первое видео!")

    # Удаляем локальное видео после отправки
    os.remove(video_path)

    # Кнопка для перехода к следующему шагу
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Дальше", callback_data="next_1")
    keyboard.add(button)

    # Отправляем кнопку
    await bot.send_message(chat_id, "Нажми кнопку, чтобы продолжить.", reply_markup=keyboard)

# Регистрация обработчиков с использованием Router
@router.message(Command('start'))  # Используем Command фильтр
async def send_welcome(message: types.Message):
    # Начинаем с первого шага
    await send_step(message.chat.id)

# Обработка кнопки "Дальше"
@router.callback_query(lambda c: c.data == "next_1")
async def next_step(callback_query: types.CallbackQuery):
    # Переход к следующему шагу (на данный момент просто подтверждаем)
    await callback_query.message.edit_text("Переход к следующему шагу...")

# Добавляем маршрутизатор в диспетчер
dp.include_router(router)

async def main():
    # Запускаем бота
    await dp.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
