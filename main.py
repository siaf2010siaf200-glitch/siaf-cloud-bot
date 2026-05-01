import os
import threading
from flask import Flask
import telebot
from telebot import types

# 1. التوكن من Railway Variables
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 2. سيرفر Flask عشان Railway ميقفلش
app = Flask(__name__)

@app.route('/')
def home():
    return "🦍 Siaf Bot شغال تمام"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# 3. اوامر البوت
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🦍 اهلا يا CEO\nالبوت شغال تمام\nاكتب /help")

@bot.message_handler(commands=['help'])
def help_command(message):
    text = """
📋 الاوامر المتاحة:

 /start - تشغيل البوت
 /help - المساعدة
 /btc - سعر البتكوين
 /gen_code - توليد كود

اكتب الامر اللي عايزه 👇
"""
    bot.reply_to(message, text)

@bot.message_handler(commands=['btc'])
def btc_price(message):
    bot.reply_to(message, "₿ سعر البتكوين: 65,000$ 💵")

@bot.message_handler(commands=['gen_code'])
def gen_code(message):
    try:
        parts = message.text.split()
        if len(parts) > 1:
            days = parts[1]
            bot.reply_to(message, f"✅ تم توليد كود لمدة {days} يوم")
        else:
            bot.reply_to(message, "استخدم: /gen_code 30")
    except:
        bot.reply_to(message, "فيه مشكلة جرب تاني")

# 4. اي رسالة عادية
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text == "بتكوين" or message.text == "بتكوين ₿":
        bot.reply_to(message, "₿ سعر البتكوين: 65,000$ 💵")
    elif message.text == "دولار" or message.text == "دولار 💵":
        bot.reply_to(message, "💵 سعر الدولار: 48 جنيه")
    elif message.text == "شارت" or message.text == "شارت 📊":
        bot.reply_to(message, "📊 شارت البتكوين:\nhttps://www.tradingview.com/symbols/BTCUSD/")
    else:
        bot.reply_to(message, "اكتب /help عشان تشوف الاوامر المتاحة")

# 5. تشغيل الاتنين مع بعض
if __name__ == "__main__":
    print("🦍 بوت تليجرام بدأ شغل")
    # شغل Flask في ثريد منفصل
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    # شغل البوت
    bot.infinity_polling()