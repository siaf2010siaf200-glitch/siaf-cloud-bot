import telebot
import os
from flask import Flask
import threading

TOKEN='8434129325:AAFGdaOG2KvwHrQ7LoyHaKZRBZZUNSnG41Y''
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🦍 انا شغال 24/7 يا CEO من السحابة ☁️")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@app.route('/')
def home():
    return "Bot is running"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)