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

# ========== الدوال ==========
def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_btc_price():
    try:
        r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        price = r.json()['bitcoin']['usd']
        return f"₿ سعر البتكوين: {price:,.0f}$ 💵"
    except:
        return "❌ مش عارف اجيب السعر دلوقتي"

def get_usd_price():
    try:
        r = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        egp = r.json()['rates']['EGP']
        return f"💵 الدولار الأمريكي: {egp:.2f} جنيه مصري\n💰 تحديث لايف"
    except:
        return "❌ مش عارف اجيب سعر الدولار دلوقتي"

# ========== الاوامر ==========
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🦍 اهلا يا CEO\nالبوت شغال تمام\nدوس على الازرار تحت او اكتب /help")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = """📋 الاوامر المتاحة:

🔹 /start - تشغيل البوت
🔹 /help - المساعدة
🔹 /btc - سعر البتكوين
🔹 /gen_code 30 - توليد كود لمدة 30 يوم

او استخدم الازرار تحت 👇"""
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

# ========== الازرار التسعة ==========
@bot.message_handler(func=lambda m: 'بتكوين' in m.text)
def btc_btn(message):
    bot.reply_to(message, get_btc_price())

@bot.message_handler(func=lambda m: 'دولار' in m.text)
def usd_btn(message):
    bot.reply_to(message, get_usd_price())

@bot.message_handler(func=lambda m: 'شارت' in m.text)
def chart_btn(message):
    bot.reply_to(message, "📊 شارت البتكوين لايف:\nhttps://www.tradingview.com/chart/?symbol=BTCUSD")

@bot.message_handler(func=lambda m: 'أخبار' in m.text)
def news_btn(message):
    bot.reply_to(message, "📰 اخر اخبار الكريبتو:\nhttps://ar.cointelegraph.com\n\nhttps://www.coindesk.com")

@bot.message_handler(func=lambda m: 'تحويل' in m.text)
def convert_btn(message):
    bot.reply_to(message, "💱 تحويل العملات:\nاكتب كده مثلا:\n`100 دولار كم جنيه`\n\nاو:\n`50 يورو كم دولار`")

@bot.message_handler(func=lambda m: 'BTC تنبيه' in m.text or 'تنبيه BTC' in m.text)
def btc_alert_btn(message):
    bot.reply_to(message, "🔔 تنبيهات البتكوين:\nلسه تحت التطوير يا CEO\nقريب هتقدر تحدد سعر وينبهك")

@bot.message_handler(func=lambda m: 'تنبيه دولار' in m.text or 'دولار تنبيه' in m.text)
def usd_alert_btn(message):
    bot.reply_to(message, "🔔 تنبيهات الدولار:\nلسه تحت التطوير\nقريب هتقدر تحدد سعر وينبهك")

@bot.message_handler(func=lambda m: 'وضع AI' in m.text or 'AI' in m.text)
def ai_btn(message):
    bot.reply_to(message, "🤖 وضع الذكاء الاصطناعي:\nقريب هنضيف ChatGPT للبوت\nتابعنا يا CEO")

@bot.message_handler(func=lambda m: 'أذكار' in m.text)
def azkar_btn(message):
    azkar = [
        "🤲 سبحان الله وبحمده سبحان الله العظيم",
        "🤲 لا إله إلا الله وحده لا شريك له",
        "🤲 استغفر الله العظيم وأتوب إليه",
        "🤲 الحمد لله رب العالمين"
    ]
    bot.reply_to(message, random.choice(azkar))

@bot.message_handler(func=lambda m: 'المساعدة' in m.text)
def help_btn(message):
    help_cmd(message)

# ========== Flask للـ Railway ==========
@app.route('/')
def home():
    return "Siaf BTC Alert Bot is running ✅"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    print("🦍 بوت Siaf BTC Alert بدأ شغل")
    bot.infinity_polling()