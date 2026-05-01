import os
import telebot
import threading
import random
import string
import requests
from flask import Flask

TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    raise Exception("Bot token is not defined")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# دالة توليد كود عشوائي
def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# دالة جلب سعر البتكوين
def get_btc_price():
    try:
        r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        price = r.json()['bitcoin']['usd']
        return f"₿ سعر البتكوين: {price:,.0f}$ 💵"
    except:
        return "❌ مش عارف اجيب السعر دلوقتي"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🦍 اهلا يا CEO\nالبوت شغال تمام\nاكتب /help عشان تشوف الاوامر")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = """📋 الاوامر المتاحة:

🔹 /start - تشغيل البوت
🔹 /help - المساعدة
🔹 /btc - سعر البتكوين
🔹 /gen_code 30 - توليد كود لمدة 30 يوم

اكتب الامر اللي عايزه 👇"""
    bot.reply_to(message, text)

@bot.message_handler(commands=['btc'])
def btc_price(message):
    bot.reply_to(message, get_btc_price())

@bot.message_handler(commands=['gen_code'])
def gen_code(message):
    try:
        days = message.text.split()[1]
        code = generate_code()
        bot.reply_to(message, f"✅ تم توليد كود:\n\n`{code}`\n\nصالح لمدة: {days} يوم")
    except:
        bot.reply_to(message, "❌ استخدم كده: /gen_code 30")

@bot.message_handler(func=lambda message: 'بتكوين' in message.text.lower())
def btc_text(message):
    bot.reply_to(message, get_btc_price())

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    print("🦍 بوت تليجرام بدأ شغل")
    bot.infinity_polling()