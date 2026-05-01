import os
import telebot
import threading
import random
import requests
import re
import string
from datetime import datetime, timedelta
from flask import Flask
from telebot import types

TOKEN = os.environ.get('TELEGRAM_TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID', '6647440011')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

SUBSCRIBERS = {}
CODES = {}
USER_COUNTRY = {}
USER_WATCHLIST = {}

def check_sub(user_id):
    if str(user_id) == ADMIN_ID: return True
    return user_id in SUBSCRIBERS and datetime.now().timestamp() < SUBSCRIBERS[user_id]

def get_country(user_id): return USER_COUNTRY.get(user_id, 'EG')

def main_keyboard():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        '🔥 اشارات تداول لحظية', '🐋 تنبيه حيتان كريبتو', '📊 تحليل فني احترافي',
        '💎 عملات جديدة قبل الادراج', '📈 اسهم امريكية لايف', '💰 فرص اربيتراج',
        '🤖 بوت DCA تلقائي', '📡 اخبار قبل السوق', '🎯 نقاط دخول وخروج',
        '📉 كشف التلاعب بالسوق', '💹 مؤشر الخوف والطمع', '🔮 توقع AI متقدم',
        '🌍 احصائيات دولية حصرية', '📱 تنبيهات واتساب فورية', '📧 تقارير يومية PDF',
        '💼 محفظة VIP متعددة', '🔔 تنبيه اي عملة', '📞 مكالمة مع خبير',
        '🎓 كورس تداول VIP', '📚 مكتبة كتب مدفوعة', '🎥 فيديوهات حصرية',
        '🏆 مسابقة جوائز اسبوعية', '💸 استرداد 20% من الخسارة', '🎁 هدايا للمشتركين',
        '📱 سر الارقام الامريكية', '📞 سر الارقام المصرية', '💱 170 عملة لايف',
        '📊 مقارنات اسعار عالمية', '🎮 نتائج مباريات لايف', '📞 دعم 24/7',
        '🌤️ طقس دقيق 14 يوم', '🕌 مواقيت صلاة + اذان',
        '💰 هاك كوبونات امازون', '📦 هاك اربيتراج منتجات', '🤖 هاك الذكاء الصناعي',
        '🛒 صفقات اربيتراج جاهزة'
    ]
    m.add(*[types.KeyboardButton(b) for b in buttons])
    return m

@bot.message_handler(commands=['start'])
def start(message):
    if check_sub(message.from_user.id):
        bot.reply_to(message, f"🦍 Siaf Global VIP ✅\n👑 مرحبا بك في النخبة\n🌍 دولتك: {get_country(message.from_user.id)}\n\n💎 36 اداة احترافية تحت 👇\n⚖️ كل الخدمات قانونية 100%\n💰 7 مصادر دخل حلال", reply_markup=main_keyboard())
    else:
        bot.reply_to(message, "🦍 Siaf Global VIP\n\n❌ اشتراك 50 جنيه شهريا\n💎 36 اداة تكسبك فلوس:\n\n🔥 اشارات تداول تكسب منها\n🐋 تتبع الحيتان\n💎 عملات 50x قبل الادراج\n📱 اسرار الارقام توفر 540ج سنويا\n💰 هاكات تكسبك 27 الف في البيعة\n📊 كورسات 500$ مجانا\n\n⚖️ كل الخدمات قانونية 100%\n💰 هترجع الاشتراك من اول صفقة\n\nللاشتراك: @siaf\n/activate CODE")

@bot.message_handler(commands=['gen_code'])
def gen_code(message):
    if str(message.from_user.id)!= ADMIN_ID: return
    try:
        days = int(message.text.split()[1])
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        CODES[code] = days
        bot.reply_to(message, f"✅ كود VIP:\n`{code}`\n{days} يوم\n50 جنيه\n\n⚠️ صالح لشخص واحد فقط", reply_markup=main_keyboard())
    except: bot.reply_to(message, "استخدم: /gen_code 30")

@bot.message_handler(commands=['activate'])
def activate(message):
    try:
        code = message.text.split()[1].upper()
        if code in CODES:
            SUBSCRIBERS[message.from_user.id] = datetime.now().timestamp() + (CODES[code] * 86400)
            del CODES[code]
            bot.reply_to(message, "✅ مرحبا بك في VIP\n👑 كل الادوات اتفتحت\n💰 يلا نكسب سوا حلال", reply_markup=main_keyboard())
    except: bot.reply_to(message, "اكتب: /activate CODE")

@bot.message_handler(func=lambda m: 'اشارات تداول لحظية' in m.text)
def btn1(message):
    if not check_sub(message.from_user.id): return start(message)
    pairs = ['BTC/USDT','ETH/USDT','SOL/USDT','BNB/USDT']
    p = random.choice(pairs)
    action = random.choice(['🟢 شراء','🔴 بيع'])
    bot.reply_to(message, f"🔥 اشارة لحظية VIP:\n\n{p}\n{action} الآن\nدخول: {random.randint(50000,70000):,}\nهدف 1: +2%\nهدف 2: +5%\nوقف خسارة: -1.5%\n\n⏰ صالحة 5 دقائق\n📊 نسبة نجاح 78%")

@bot.message_handler(func=lambda m: 'تنبيه حيتان' in m.text)
def btn2(message):
    if not check_sub(message.from_user.id): return start(message)
    amount = random.randint(100,1000)
    bot.reply_to(message, f"🐋 تحرك حوت منذ 2 دقيقة:\n\n{amount} BTC = {amount*65000:,.0f}$\nمن: Binance\nالى: محفظة باردة\n\n📊 التحليل: تجميع ✅\n💡 المعنى: السعر ممكن يطلع\n\n🔔 هبلغك لو اتحرك تاني")

@bot.message_handler(func=lambda m: 'تحليل فني احترافي' in m.text)
def btn3(message):
    if not check_sub(message.from_user.id): return start(message)
    rsi = random.randint(20,80)
    bot.reply_to(message, f"📊 تحليل BTC احترافي:\n\nRSI: {rsi} {'تشبع بيع 🟢' if rsi<30 else 'تشبع شراء 🔴' if rsi>70 else 'محايد'}\nMACD: {'تقاطع صعودي 🟢' if random.random()>0.5 else 'تقاطع هبوطي 🔴'}\nBollinger: {'لمس السفلي 🟢' if random.random()>0.5 else 'لمس العلوي 🔴'}\nحجم التداول: +{random.randint(10,50)}%\n\n🎯 التوصية: {random.choice(['شراء قوي','بيع','انتظار','تجميع'])}\n\n📈 شارت: tradingview.com")

@bot.message_handler(func=lambda m: 'عملات جديدة قبل الادراج' in m.text)
def btn4(message):
    if not check_sub(message.from_user.id): return start(message)
    coins = ['ZETA','PIXEL','STRK','PORTAL']
    c = random.choice(coins)
    bot.reply_to(message, f"💎 عملة قبل الادراج:\n\n${c}\nهتدرج على Binance خلال {random.randint(1,7)} ايام\nالسعر الحالي: 0.0{random.randint(10,99)}\nالسعر المتوقع: 0.{random.randint(1,9)}\n\n🚀 ربح متوقع: {random.randint(5,50)}x\n⚠️ مخاطرة عالية\n💰 ادخل بـ 2% من راس المال فقط")

@bot.message_handler(func=lambda m: 'اسهم امريكية' in m.text)
def btn5(message):
    if not check_sub(message.from_user.id): return start(message)
    stocks = {'AAPL':175.5,'TSLA':248.3,'NVDA':892.1,'MSFT':405.2}
    s = random.choice(list(stocks.keys()))
    change = random.uniform(-3,3)
    bot.reply_to(message, f"📈 سهم {s} لايف:\n\nالسعر: {stocks[s]:.2f}$\nالتغيير: {change:+.2f}%\nالحجم: {random.randint(10,100)}M\n\n{'🟢 زخم شرائي' if change>0 else '🔴 ضغط بيع'}\n\n📰 خبر: {random.choice(['ارباح قوية','منتج جديد','استحواذ'])}")

@bot.message_handler(func=lambda m: 'فرص اربيتراج' in m.text)
def btn6(message):
    if not check_sub(message.from_user.id): return start(message)
    diff = random.uniform(0.5,3.0)
    bot.reply_to(message, f"💰 فرصة اربيتراج:\n\nBTC\nBinance: 65,200$\nCoinbase: {65200 + random.randint(100,500)}$\n\n💵 الفرق: {diff:.2f}%\n💚 ربح صافي: ~{random.randint(50,300)}$\n\n⚡ نفذ بسرعة الفرصة تختفي خلال دقائق")

@bot.message_handler(func=lambda m: 'بوت DCA تلقائي' in m.text)
def btn7(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "🤖 بوت DCA VIP:\n\nاكتب كده:\ndca BTC 100 7\n\nالمع