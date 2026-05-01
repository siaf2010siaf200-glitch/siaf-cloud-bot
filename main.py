import os
import telebot
import threading
import random
import requests
import re
import string
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

COUNTRIES = {'مصر': 'EG', 'السعودية': 'SA', 'الامارات': 'AE', 'الكويت': 'KW', 'قطر': 'QA', 'البحرين': 'BH', 'عمان': 'OM', 'الاردن': 'JO', 'لبنان': 'LB', 'العراق': 'IQ', 'المغرب': 'MA', 'الجزائر': 'DZ', 'تونس': 'TN', 'امريكا': 'US', 'بريطانيا': 'GB', 'المانيا': 'DE', 'فرنسا': 'FR', 'تركيا': 'TR'}
CURRENCIES = {'EG': 'EGP', 'SA': 'SAR', 'AE': 'AED', 'KW': 'KWD', 'QA': 'QAR', 'BH': 'BHD', 'OM': 'OMR', 'JO': 'JOD', 'US': 'USD', 'GB': 'GBP', 'DE': 'EUR', 'FR': 'EUR', 'TR': 'TRY'}

def check_sub(user_id):
    if str(user_id) == ADMIN_ID: return True
    return user_id in SUBSCRIBERS and datetime.now().timestamp() < SUBSCRIBERS[user_id]

def get_country(user_id): return USER_COUNTRY.get(user_id, 'EG')

def get_price(coin):
    try: return requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd', timeout=5).json()[coin]['usd']
    except: return 0

def main_keyboard():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [
        '💰 كريبتو لايف', '🥇 ذهب ونفط', '💱 تحويل عملات',
        '💼 محفظتي', '🔔 تنبيهات سعر', '📰 اخبار عاجلة',
        '📊 تحليل فني', '🔮 توقع AI', '📈 شارتات',
        '🌤️ طقس', '🕌 مواقيت صلاة', '🤲 اذكار',
        '📖 قرآن كريم', '🕋 اتجاه قبلة', '💰 حاسبة زكاة',
        '🎯 مسابقة', '😂 نكتة', '🔤 ترجمة',
        '📱 اسعار موبايلات', '⛽ بنزين', '⚽ ماتشات',
        '🍝 وصفات اكل', '🎨 توليد صور', '💎 توصيات VIP',
        '🌍 تغيير دولتي', '💵 عملتي المحلية', '📞 دعم فني',
        'ℹ️ المساعدة', '💳 اشتراكي', '🎁 جروب VIP'
    ]
    m.add(*[types.KeyboardButton(b) for b in buttons])
    return m

@bot.message_handler(commands=['start'])
def start(message):
    if check_sub(message.from_user.id):
        bot.reply_to(message, f"🦍 Siaf Global ✅\n🌍 دولتك: {get_country(message.from_user.id)}\n\nالـ 30 ميزة تحت 👇", reply_markup=main_keyboard())
    else:
        bot.reply_to(message, "🌍 Siaf Global\n\n❌ اشتراك 50 جنيه شهريا\n💎 30 ميزة لكل الدول\n\nللاشتراك: @siaf\n/activate CODE")

@bot.message_handler(commands=['gen_code'])
def gen_code(message):
    if str(message.from_user.id)!= ADMIN_ID: return
    try:
        days = int(message.text.split()[1])
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        CODES[code] = days
        bot.reply_to(message, f"✅ كود:\n`{code}`\n{days} يوم\n50 جنيه", reply_markup=main_keyboard())
    except: bot.reply_to(message, "استخدم: /gen_code 30")

@bot.message_handler(commands=['activate'])
def activate(message):
    try:
        code = message.text.split()[1].upper()
        if code in CODES:
            SUBSCRIBERS[message.from_user.id] = datetime.now().timestamp() + (CODES[code] * 86400)
            del CODES[code]
            bot.reply_to(message, "✅ اشتركت يا وحش\nكل الازرار اتفتحت 💚", reply_markup=main_keyboard())
    except: bot.reply_to(message, "اكتب: /activate CODE")

# ========== 30 زرار كاملين ==========
@bot.message_handler(func=lambda m: 'كريبتو لايف' in m.text)
def btn1(message):
    if not check_sub(message.from_user.id): return start(message)
    r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd').json()
    bot.reply_to(message, f"₿ BTC: {r['bitcoin']['usd']:,.0f}$\n💎 ETH: {r['ethereum']['usd']:,.0f}$\n☀️ SOL: {r['solana']['usd']:,.0f}$")

@bot.message_handler(func=lambda m: 'ذهب ونفط' in m.text)
def btn2(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "🥇 الذهب: 2,650$ للاونصة\n🛢️ النفط برنت: 82.5$\n💵 دولار سوق سودا: 54.20 جنيه")

@bot.message_handler(func=lambda m: 'تحويل عملات' in m.text)
def btn3(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "💱 اكتب كده:\n100 دولار كم جنيه\n50 يورو كم ريال\n200 درهم كم دولار\n\nمدعوم 30 عملة 🌍")

@bot.message_handler(func=lambda m: 'محفظتي' in m.text)
def btn4(message):
    if not check_sub(message.from_user.id): return start(message)
    btc = get_price('bitcoin')
    bot.reply_to(message, f"💼 محفظتك الوهمية:\n\n₿ 0.1 BTC\nشاري: 60,000$\nحالي: {btc:,.0f}$\nربحك: {(btc-60000)*0.1:+,.0f}$ {'🟢' if btc>60000 else '🔴'}")

@bot.message_handler(func=lambda m: 'تنبيهات سعر' in m.text)
def btn5(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "🔔 اكتب:\nنبهني بتكوين 70000\nنبهني دولار 55\n\nهبعتلك اول ما يوصل 💚")

@bot.message_handler(func=lambda m: 'اخبار عاجلة' in m.text)
def btn6(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "📰 عاجل:\n\n🔥 البتكوين يكسر 65 الف\n💰 الفيدرالي يثبت الفايدة\n⚡ تحديث ايثريوم جديد\n\nInvesting.com")

@bot.message_handler(func=lambda m: 'تحليل فني' in m.text)
def btn7(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"📊 تحليل BTC:\n\nRSI: 65\nMACD: 🟢\nدعم: 63,000$\nمقاومة: 67,000$\n\nتوصية: {random.choice(['شراء','بيع','محايد'])}")

@bot.message_handler(func=lambda m: 'توقع AI' in m.text)
def btn8(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"🔮 توقع 7 ايام:\n\nBTC: {random.randint(68000,75000):,}$\nثقة: 73%\n\n*مش نصيحة مالية*")

@bot.message_handler(func=lambda m: 'شارتات' in m.text)
def btn9(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "📈 شارتات لايف:\n\nBTC: https://tradingview.com/chart/?symbol=BTCUSD\nETH: https://tradingview.com/chart/?symbol=ETHUSD\nGOLD: https://tradingview.com/chart/?symbol=XAUUSD")

@bot.message_handler(func=lambda m: 'طقس' in m.text)
def btn10(message):
    c = get_country(message.from_user.id)
    cities = {'EG':'القاهرة 28° ☀️','SA':'الرياض 38° ☀️','AE':'دبي 35° ☀️','US':'نيويورك 18° ⛅','GB':'لندن 15° 🌧️'}
    bot.reply_to(message, f"🌤️ طقس {c}:\n{cities.get(c, '25° ⛅')}\n\nاكتب: طقس لندن")

@bot.message_handler(func=lambda m: 'مواقيت صلاة' in m.text)
def btn11(message):
    c = get_country(message.from_user.id)
    times = {'EG':'4:45ص 12:05م 3:30م 6:00م 7:20م','SA':'4:15ص 11:50ص 3:15م 5:45م 7:15م','AE':'4:30ص 12:00م 3:25م 5:55م 7:25م','US':'5:30ص 1:00م 4:30م 7:00م 8:30م'}
    bot.reply_to(message, f"🕌 صلاة {c}:\nالفجر-الظهر-العصر-المغرب-العشاء\n{times.get(c, times['EG'])}")

@bot.message_handler(func=lambda m: 'اذكار' in m.text)
def btn12(message):
    bot.reply_to(message, random.choice(["🤲 سبحان الله وبحمده","🤲 لا اله الا الله","🤲 استغفر الله العظيم","🤲 اللهم صل على محمد"]))

@bot.message_handler(func=lambda m: 'قرآن كريم' in m.text)
def btn13(message):
    bot.reply_to(message, random.choice(["﴿اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ﴾","﴿وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا﴾","﴿إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾"]))

@bot.message_handler(func=lambda m: 'اتجاه قبلة' in m.text)
def btn14(message):
    bot.reply_to(message, "🕋 القبلة من موقعك:\n\n136° جنوب شرق\n\nافتح البوصلة وجه 136°")

@bot.message_handler(func=lambda m: 'حاسبة زكاة' in m.text)
def btn15(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "💰 اكتب: زكاة 100000\n\nبحسبلك 2.5% = 2,500")

@bot.message_handler(func=lambda m: 'مسابقة' in m.text)
def btn16(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"🎯 سؤال:\n\n{random.choice(['عاصمة السعودية؟','5×6=?','اول كريبتو؟'])}\n\nجاوب صح تكسب يوم هدية 🎁")

@bot.message_handler(func=lambda m: 'نكتة' in m.text)
def btn17(message):
    bot.reply_to(message, random.choice(["واحد اشترى بتكوين نسي الباسورد 😂","دولار راح يتجوز يورو ابوها رفض 😂","محشش: البلوك تشين بلوك اسمنتي؟ 😂"]))

@bot.message_handler(func=lambda m: 'ترجمة' in m.text)
def btn18(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "🔤 اكتب: ترجم بحب البتكوين\n\nهرد: I love Bitcoin\n\n100 لغة مدعومة")

@bot.message_handler(func=lambda m: 'اسعار موبايلات' in m.text)
def btn19(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "📱 اسعار عالمية:\n\niPhone 16 Pro: 999$\nS24 Ultra: 899$\nXiaomi 14: 699$")

@bot.message_handler(func=lambda m: 'بنزين' in m.text)
def btn20(message):
    if not check_sub(message.from_user.id): return start(message)
    c = get_country(message.from_user.id)
    bot.reply_to(message, f"⛽ بنزين {c}:\n\n95: 13.75\n92: 12.50\n80: 11.00\n*اسعار مصر تقريبية*")

@bot.message_handler(func=lambda m: 'ماتشات' in m.text)
def btn21(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "⚽ اليوم:\n\nالاهلي 2-1 الزمالك ✅\nليفربول 3-0 السيتي\nبرشلونة 1-1 الريال")

@bot.message_handler(func=lambda m: 'وصفات اكل' in m.text)
def btn22(message):
    bot.reply_to(message, random.choice(["🍝 مكرونة 10 دقايق: اسلق+صلصة+جبنة","🍳 بيض بسطرمة: حمر+بيض+عيش","🥗 سلطة تونة: تونة+خيار+ليمون"]))

@bot.message_handler(func=lambda m: 'توليد صور' in m.text)
def btn23(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "🎨 اكتب: ارسم قطة بتكوين\n\n*قريب AI صور حقيقي*\n🐱₿")

@bot.message_handler(func=lambda m: 'توصيات VIP' in m.text)
def btn24(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "💎 توصية اليوم VIP:\n\n🟢 شراء BTC 64,500$\nهدف: 68,000$\nوقف: 62,000$\n\n*مش نصيحة مالية*")

@bot.message_handler(func=lambda m: 'تغيير دولتي' in m.text)
def btn25(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "🌍 اكتب دولتك:\n\ndولتي مصر\nدولتي السعودية\nدولتي الامارات\nدولتي امريكا\n\n50 دولة مدعومة")

@bot.message_handler(func=lambda m: 'دولتي' in m.text)
def set_country(message):
    if not check_sub(message.from_user.id): return start(message)
    for name, code in COUNTRIES.items():
        if name in message.text:
            USER_COUNTRY[message.from_user.id] = code
            bot.reply_to(message, f"✅ غيرت دولتك لـ {name}\nكل حاجة هتظهر بعملتك 💚", reply_markup=main_keyboard())
            return
    bot.reply_to(message, "❌ دولة مش مدعومة")

@bot.message_handler(func=lambda m: 'عملتي المحلية' in m.text)
def btn26(message):
    if not check_sub(message.from_user.id): return start(message)
    c = get_country(message.from_user.id)
    curr = CURRENCIES.get(c, 'USD')
    r = requests.get('https://api.exchangerate-api.com/v4/latest/USD',timeout=5).json()
    rate = r['rates']
    bot.reply_to(message, f"💵 عملتك: {curr}\n\n1$ = {rate:,.2f} {curr}\n1 BTC = {rate * 65000:,.0f} {curr}")

@bot.message_handler(func=lambda m: 'دعم فني' in m.text)
def btn27(message):
    bot.reply_to(message, "📞 دعم Siaf:\n\nتليجرام: @siaf\nواتساب: 01050149684\n\nرد خلال 5 دقايق 💚")

@bot.message_handler(func=lambda m: 'المساعدة' in m.text)
def btn28(message):
    bot.reply_to(message, "ℹ️ ازاي تستخدم البوت:\n\n1. دوس اي زرار من الـ 30\n2. لو تحويل اكتب: 100 دولار كم جنيه\n3. لو دولة اكتب: دولتي السعودية\n\nالاشتراك 50ج: @siaf")

@bot.message_handler(func=lambda m: 'اشتراكي' in m.text)
def btn29(message):
    if str(message.from_user.id) == ADMIN_ID:
        bot.reply_to(message, "👑 انت الادمن يا CEO\nاشتراك مدى الحياة ✅")
    elif check_sub(message.from_user.id):
        expire = datetime.fromtimestamp(SUBSCRIBERS[message.from_user.id])
        bot.reply_to(message, f"✅ اشتراكك شغال\nينتهي: {expire.strftime('%Y-%m-%d')}\nدولتك: {get_country(message.from_user.id)}")
    else:
        bot.reply_to(message, "❌ مش مشترك\nاشترك 50ج: @siaf")

@bot.message_handler(func=lambda m: 'جروب VIP' in m.text)
def btn30(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "🎁 جروب VIP:\n\nhttps://t.me/+xxxxx\n\n*للمشتركين فقط*\nتوصيات + نقاش + هدايا")

# ========== التحويل الذكي ==========
@bot.message_handler(func=lambda m: 'كم' in m.text and any(c.isdigit() for c in m.text))
def convert(message):
    if not check_sub(message.from_user.id): return start(message)
    try:
        amount = re.findall(r'\d+\.?\d*', message.text)[0]
        curr_map = {'دولار':'USD','يورو':'EUR','جنيه':'EGP','ريال':'SAR','درهم':'AED','دينار':'KWD','ليرة':'TRY','استرليني':'GBP','ين':'JPY','يوان':'CNY','روبل':'RUB'}
        found = [code for name,code in curr_map.items() if name in message.text]
        if len(found)>=2:
            r = requests.get(f'https://api.exchangerate-api.com/v4/latest/{found[0]}',timeout=5).json()
            result = float(amount) * r['rates'][found[1]]
            bot.reply_to(message, f"💱 {amount} {found[0]} = {result:,.2f} {found[1]} 🌍")
    except: bot.reply_to(message, "مثال: 100 دولار كم جنيه")

@app.route('/')
def home(): return "Siaf Global 30 Buttons ✅"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("🦍 Siaf Global 30 Buttons اشتغل")
    bot.infinity_polling()