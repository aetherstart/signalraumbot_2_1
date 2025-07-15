import os
import telebot
from flask import Flask, request

API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  # in Replit als Secret setzen
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Beispielantwort
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hey! Ich bin aktiv und warte auf deine Befehle.")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"Du hast gesagt: {message.text}")

# Webhook-Endpunkt
@app.route(f"/{API_TOKEN}", methods=["POST"])
def receive_update():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# Root check (optional)
@app.route("/", methods=["GET"])
def index():
    return "Bot läuft!", 200

# Start
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
