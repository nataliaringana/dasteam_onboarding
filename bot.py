import telebot
import os
from flask import Flask, request

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

# Handler für das /start-Kommando
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hallo und willkommen! Wie kann ich dir helfen?")

# Webhook-Endpunkt
@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Webhook-Setup (wird beim Start ausgeführt)
bot.remove_webhook()
bot.set_webhook(url="https://DEIN-RENDER-URL/")  # Ersetze DEIN-RENDER-URL mit deiner tatsächlichen URL

# Hinweis: Den Flask-Server starten wir über gunicorn (nicht über app.run)
