import telebot
import os
from flask import Flask, request

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://api.render.com/deploy/srv-cvn8id1r0fns738jm7l0?key=8roahJ-SX3w")
    app.run(host="0.0.0.0", port=5000)
