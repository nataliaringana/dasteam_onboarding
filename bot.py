import os
import telebot

API_TOKEN = os.getenv("API_TOKEN")  # Token aus Umgebungsvariable laden
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hallo! Ich bin dein Telegram-Bot.")

bot.polling()
