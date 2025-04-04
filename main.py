import os
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
dp = Dispatcher(bot, storage=storage)

# Создаем Router для регистрации обработчиков
router = Router()

# Текст для первого шага
step_1_text = """
Hallo liebe/r {Vorname}! 😊

🎉 HERZLICH WILLKOMMEN IM TEAM! 🎉
Ich freue mich, dich auf deinem Weg bei RINGANA zu begleiten. Gemeinsam schaffen wir Großes – mit Leichtigkeit und Freude.
"""

# Функция для отправки текста и кнопки
async def send_step(chat_id):
    # Отправляем текст
    await bot.send_message(chat_id, step_1_text.format(Vorname="User"))

    # Кнопка для перехода к следующему шагу
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Дальше", callback_data="next_1")
    keyboard.add(button)

    # Отправляем кнопку
    await bot.send_message(chat_
