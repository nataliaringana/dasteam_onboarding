from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я ваш первый Telegram-бот.')

# Основная часть программы
if __name__ == '__main__':
    # Токен бота
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    # URL вашего сервиса
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # например, "https://your-app-name.onrender.com"

    # Создайте приложение бота
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавьте обработчик команды /start
    app.add_handler(CommandHandler('start', start))

    # Установите Webhook
    app.run_webhook(
        listen="0.0.0.0",  # Слушаем все IP-адреса
        port=int(os.getenv('PORT', 8443)),  # Используем порт из Render
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )