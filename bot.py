import logging
from flask import Flask, request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Flask app
app = Flask(__name__)

# Telegram bot token
TOKEN = "7234160422:AAFjlAUch607gd-l_nA_V20sg0VcR5REK-A"
bot = telegram.Bot(token=TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

def start(update, context):
    user = update.effective_user
    name = user.first_name if user.first_name else "liebe/r Teilnehmer/in"

    text = (f"Hallo liebe {name}! ❤\n"
            "Herzlich willkommen im Team! Ich freue mich unglaublich, dich auf deinem Weg bei RINGANA zu begleiten. Gemeinsam schaffen wir Großes und erschaffen ein erfolgreiches Business in Leichtigkeit und Freude!\n"
            "Willkommensvideo Schanna: https://boards.com/a/7FjT7.RRhfze\n"
            "Lass uns Schritt für Schritt starten. Alles, was du brauchst, bekommst du hier.\n"
            "Bist du bereit? Klicke auf \u201eLos geht\u2019s\u201c, und wir starten!")

    keyboard = [[InlineKeyboardButton("Los geht's", callback_data='step1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)

def handle_callback(update, context):
    query = update.callback_query
    query.answer()

    responses = {
        'step1': {
            'text': ("Dein erster Schritt: Hol dir Inspiration und fühl dich in die Vibes unseres Teams ein. "
                     "Schau dir dieses kurze Video an: https://youtu.be/XclhutKFG4k\n"
                     "Klicke auf \u201eWeiter\u201c, sobald du das Video angesehen hast."),
            'keyboard': [[InlineKeyboardButton("Weiter", callback_data='step2')]]
        },
        'step2': {
            'text': ("Mache dir nun Gedanken, warum du dich für die Partnerschaft entschieden hast, "
                     "welche Ziele du mit RINGANA erreichen möchtest und wie möchtest du von mir als Mentor begleitet werden?\n"
                     "Schreibe es auf und schicke es an deinen Mentor.\n"
                     "Sobald du fertig bist, klicke auf \u201eAbgeschickt\u201c."),
            'keyboard': [[InlineKeyboardButton("Abgeschickt", callback_data='step3')]]
        },
        'step3': {
            'text': ("Danke, dass du deine Gedanken geteilt hast! Ich freue mich, dich auf diesem Weg zu unterstützen.\n"
                     "Als nächstes steht der Welcome Call an. Es ist ein wichtiger Einstieg, um das Unternehmen RINGANA "
                     "persönlich und die Basics besser kennenzulernen.\n"
                     "Melde dich hier an: https://www.ringana.com/connect/#/welcome-events\n"
                     "Klicke auf \u201eAbgeschlossen\u201c, sobald du dich angemeldet hast."),
            'keyboard': [[InlineKeyboardButton("Abgeschlossen", callback_data='step4')]]
        },
        'step4': {
            'text': ("Jetzt geht es darum, Network Marketing besser zu verstehen.\n"
                     "Das Buch \u201eDie 45 Sekunden Präsentation\u201c ist ein Klassiker.\n"
                     "Hier bekommst du die ersten 4 relevanten Kapitel (30 Min): PDF einfügen\n"
                     "Klicke auf \u201eGelesen\u201c, wenn du fertig bist."),
            'keyboard': [[InlineKeyboardButton("Gelesen", callback_data='step5')]]
        },
        'step5': {
            'text': ("Sobald deine Business Unterlagen angekommen sind, lies sie sorgfältig durch.\n"
                     "Falls du sie gerade nicht griffbereit hast, lade sie hier runter: \n"
                     "https://www.ringana.com/downloads/\n"
                     "Klicke auf \u201eFertig\u201c, wenn du sie gelesen hast."),
            'keyboard': [[InlineKeyboardButton("Fertig", callback_data='step6')]]
        },
        'step6': {
            'text': ("RINGANA bietet eine umfangreiche Online Academy.\n"
                     "Melde dich in deinem Online-Office an und starte mit den ersten Modulen.\n"
                     "Klicke auf \u201eFertig\u201c, wenn du die Kapitel \u201eFRESH start\u201c und \u201eKundengewinnung Basic\u201c durchgesehen hast."),
            'keyboard': [[InlineKeyboardButton("Fertig", callback_data='step7')]]
        },
        'step7': {
            'text': ("In unserem Team arbeiten wir selbstständig, aber nie allein!\n"
                     "1. Montags-Meeting: Jeden Montag um 20:30 Uhr.\n"
                     "2. Telegram-Gruppe: https://t.me/+LOKepksVBy42NzRi\n"
                     "3. Boards App: Frage bei deinem Mentor nach.\n"
                     "Klicke auf \u201eBeigetreten\u201c, wenn du alles erledigt hast."),
            'keyboard': [[InlineKeyboardButton("Beigetreten", callback_data='finished')]]
        },
        'finished': {
            'text': ("Glückwunsch! Du hast deinen ersten Meilenstein geschafft.\n"
                     "Als nächstes kannst du in den Kanal für Neupartnertraining beitreten."),
            'keyboard': []
        }
    }

    response = responses.get(query.data)
    if response:
        query.edit_message_text(text=response['text'], reply_markup=InlineKeyboardMarkup(response['keyboard']) if response['keyboard'] else None)

# Dispatcher setup
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(handle_callback))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

