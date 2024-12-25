from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Dispatcher
import os

app = Flask(__name__)

# Токен бота и URL Webhook
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # например, "https://your-app-name.onrender.com"

# Создаем приложение бота
bot_app = ApplicationBuilder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я работаю через Webhook!")

# Добавляем обработчики в диспетчер
bot_app.add_handler(CommandHandler("start", start))

# Устанавливаем Webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Обработчик Webhook для Telegram"""
    update = Update.de_json(request.get_json(), bot_app.bot)
    dispatcher = Dispatcher(bot_app.bot, None, use_context=True)
    dispatcher.process_update(update)
    return "OK", 200

# Главная страница (опционально)
@app.route("/")
def index():
    return "Бот работает через Webhook!"

if __name__ == "__main__":
    # Настройка Webhook
    bot_app.bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")

    # Запускаем Flask
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8443)))
