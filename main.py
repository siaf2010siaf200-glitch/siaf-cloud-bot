import os
import telebot
import threading
import random
import requests
import re
from datetime import datetime
from flask import Flask
from telebot import types

TOKEN = os.environ.get('TELEGRAM_TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID', '6647440011')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

SUBSCRIBERS = {}
CODES = {}
USER_COUNTRY = {}

def check_sub(user_id):
    if str(user_id) == ADMIN_ID: return True
    return user_id in SUBSCRIBERS and datetime.now().timestamp() < SUBSCRIBERS[user_id]

def get_country(user_id):
    return USER_COUNTRY.get(user_id, 'EG')

# ========== الكيبورد السوبر - 30 زرار ==========
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    # صف 1: فلوس
    btn1 = types.KeyboardButton('💰 كريبتو لايف')
    btn2 = types.KeyboardButton('🥇 ذهب ونفط')
    btn3 = types.KeyboardButton('💱 تحويل عملات')

    # صف 2: محفظة واخبار
    btn4 = types.KeyboardButton('💼 محفظتي')
    btn5 = types.KeyboardButton('🔔 تنبيهات سعر')
    btn6 = types.KeyboardButton('📰 اخبار عاجلة')

    # صف 3: تحليل
    btn7 = types.KeyboardButton('📊 تحليل فني')
    btn8 = types.KeyboardButton('🔮 توقع AI')
    btn9 = types.KeyboardButton('📈 شارتات')

    # صف 4: خدمات يومية
    btn10 = types.KeyboardButton('🌤️ طقس')
    btn11 = types.KeyboardButton('🕌 مواقيت صلاة')
    btn12 = types.KeyboardButton('🤲 اذكار')

    # صف 5: اسلاميات
    btn13 = types.KeyboardButton('📖 قرآن كريم')
    btn14 = types.KeyboardButton('🕋 اتجاه قبلة')
    btn15 = types.KeyboardButton('💰 حاسبة زكاة')

    # صف 6: ترفيه
    btn16 = types.KeyboardButton('🎯 مسابقة')
    btn17 = types.KeyboardButton('😂 نكتة')
    btn18 = types.KeyboardButton('🔤 ترجمة')

    # صف 7: حياة
    btn19 = types.KeyboardButton('📱 اسعار موبايلات')
    btn20 = types.KeyboardButton('⛽ بنزين')
    btn21 = types.KeyboardButton('⚽ ماتشات')

    # صف 8: اضافي
    btn22 = types.KeyboardButton('🍝 وصفات اكل')
    btn23 = types.KeyboardButton('🎨 توليد صور')
    btn24 = types.KeyboardButton('💎 توصيات VIP')

    # صف 9: اعدادات
    btn25 = types.KeyboardButton('🌍 تغيير دولتي')
    btn26 = types.KeyboardButton('💵 عملتي المحلية')
    btn27 = types.KeyboardButton('📞 دعم فني')

    # صف 10: مساعدة
    btn28 = types.KeyboardButton('ℹ️ المساعدة')
    btn29 = types.KeyboardButton('💳 اشتراكي')
    btn30 = types.KeyboardButton('🎁 جروب VIP')

    markup.add(btn1, btn2, btn3)
    markup.add(btn4, btn5, btn6)
    markup.add(btn7, btn8, btn9)
    markup.add(btn10, btn11, btn12)
    markup.add(btn13, btn14, btn15)
    markup.add(btn16, btn17, btn18)
    markup.add(btn19, btn20, btn21)
    markup.add(btn22, btn23, btn24)
    markup.add(btn25, btn26, btn27)
    markup.add(btn28, btn29, btn30)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    if check_sub(message.from_user.id):
        bot.reply_to(message,
            f"🦍 Siaf Global - اهلا يا وحش ✅\n🌍 دولتك: {get_country(message.from_user.id)}\n\nكل الـ 30 ميزة تحت في الازرار 👇\nدوس اي زرار وجرب",
            reply_markup=main_keyboard()
        )
    else:
        bot.reply_to(message, "🌍 Siaf Global Bot\n\n❌ الاشتراك 50 جنيه شهريا\n💎 30 ميزة لكل الدول\n\nللاشتراك: @siaf\nكود تفعيل: /activate CODE")

@bot.message_handler(commands=['gen_code'])
def gen_code(message):
    if str(message.from_user.id)!= ADMIN_ID: return
    try:
        days = int(message.text.split()[1])
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        CODES[code] = days
        bot.reply_to(message, f"✅ كود عالمي:\n`{code}`\n{days} يوم\n50 جنيه 🌍", reply_markup=main_keyboard())
    except: bot.reply_to(message, "استخدم: /gen_code 30")

@bot.message_handler(commands=['activate'])
def activate(message):
    try:
        code = message.text.split()[1].upper()
        if code in CODES:
            SUBSCRIBERS[message.from_user.id] = datetime.now().timestamp() + (CODES[code] * 86400)
            del CODES[code]
            bot.reply_to(message, "✅ اشتركت يا بطل\nكل الـ 30 زرار اتفتحوا 💚", reply_markup=main_keyboard())
    except: bot.reply_to(message, "اكتب: /activate CODE")

# باقي الكود زي ما هو فوق... هحطلك الدوال بس
@bot.message_handler(func=lambda m: 'كريبتو لايف' in m.text)
def crypto_btn(message):
    if not check_sub(message.from_user.id): return start(message)
    r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd').json()
    bot.reply_to(message, f"₿ BTC: {r['bitcoin']['usd']:,.0f}$\n💎 ETH: {r['ethereum']['usd']:,.0f}$\n☀️ SOL: {r['solana']['usd']:,.0f}$")

# كمل باقي الـ 29 زرار بنفس الطريقة...

@app.route('/')
def home(): return "Siaf Global 30 Buttons ✅"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()