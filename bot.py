from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я ваш первый Telegram-бот.')

# Основная часть программы
if __name__ == '__main__':
  
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
#TOKEN = '7548766470:AAFD_UCqmoWygdgK3nGHsILLGAiXd55lq00'

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))

    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()