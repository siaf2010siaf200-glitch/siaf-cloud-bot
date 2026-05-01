import os
import telebot
from flask import Flask
import threading
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# يوزرات الـ VIP - انت VIP خلاص
VIP_USERS = ['@Siaf_basuone']

# الـ 5 ادوات المجانية بس
FREE_TOOLS = [
    'الاسعار اللحظية',
    'الاخبار العاجلة',
    'التقويم الاقتصادي',
    'من نحن',
    'الدعم الفني'
]

def main_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        'الاسعار اللحظية', 'الاوامر المعلقة', 'ارباحي اليوم', 'صفقات اربيتراج جاهزة',
        'دورات تعليمية', 'متابعة الحيتان', 'دخول جماعي', 'الدخول الامن',
        'تنبيه سيولة', 'حاسبة الربح', 'تحليل السيولة', 'المستويات',
        'اشارات فورية', 'التحليل الفني', 'التحليل الزمني', 'مناطق دخول',
        'المؤشرات', 'التقويم الاقتصادي', 'الاخبار العاجلة', 'الرسوم البيانية',
        'التحليل الاساسي', 'الاسهم الامريكية', 'العملات الرقمية', 'الذهب',
        'النفط', 'السلع', 'السندات', 'المؤشرات العالمية',
        'الفوركس', 'العقود الاجلة', 'الصناديق', 'الاشتراك الشهري',
        'الدعم الفني', 'من نحن', 'سياسة الخصوصية', '💎 فحص محافظ الحيتان'
    ]
    markup.add(*[telebot.types.KeyboardButton(btn) for btn in buttons])
    return markup

def check_vip(user):
    username = f"@{user.username}" if user.username else ""
    return username in VIP_USERS

@bot.message_handler(commands=['start'])
def start(message):
    welcome = f"""
🦍 Siaf Global VIP ✅
👑 مرحبا بك في النخبة

✅ 5 ادوات مجانية للتجربة:
- الاسعار اللحظية
- الاخبار العاجلة
- التقويم الاقتصادي
- من نحن
- الدعم الفني

🔒 31 اداة احترافية للمشتركين

💎 للاشتراك دوس: الاشتراك الشهري
"""
    bot.send_message(message.chat.id, welcome, reply_markup=main_keyboard())

# ========== الادوات المجانية ==========
@bot.message_handler(func=lambda m: 'الاسعار اللحظية' in m.text)
def btn1(message):
    try:
        btc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd').json()
        price = btc['bitcoin']['usd']
        bot.reply_to(message, f"💰 BTC: ${price:,.2f}\n\n🔒 عايز كل العملات + تحليل لحظي؟ اشترك VIP")
    except:
        bot.reply_to(message, "❌ خطأ في جلب السعر")

@bot.message_handler(func=lambda m: 'الاخبار العاجلة' in m.text)
def btn19(message):
    bot.reply_to(message, """
📰 اخر خبر:
الفيدرالي يثبت الفائدة عند 5.5%

🔒 عايز اخبار لحظية 24/7 + تأثيرها على السوق؟
اشترك VIP من: الاشتراك الشهري
""")

@bot.message_handler(func=lambda m: 'التقويم الاقتصادي' in m.text)
def btn18(message):
    bot.reply_to(message, """
📅 اهم حدث اليوم:
بيانات التضخم الامريكي 3:30م بتوقيت القاهرة

🔒 عايز تنبيه قبل الخبر + توصية دخول؟
اشترك VIP
""")

@bot.message_handler(func=lambda m: 'من نحن' in m.text)
def btn34(message):
    bot.reply_to(message, """
🦍 Siaf Global
منصة التحليل رقم 1 في الشرق الاوسط

✅ 36 اداة احترافية
✅ 7 مصادر دخل حلال
✅ دعم 24/7

المؤسس: @Siaf_basuone
""")

@bot.message_handler(func=lambda m: 'الدعم الفني' in m.text)
def btn33(message):
    bot.reply_to(message, """
💬 للدعم الفني كلمنا:
تليجرام: @Siaf_basuone
واتساب: 01050149684

مواعيد العمل: 24/7 ✅
""")

# ========== زرار الاشتراك ==========
@bot.message_handler(func=lambda m: 'الاشتراك الشهري' in m.text)
def btn32(message):
    bot.reply_to(message, """
💎 الاشتراك الشهري - 10$ فقط

✅ فتح كل الـ 31 اداة المقفولة:
- صفقات اربيتراج جاهزة
- اشارات فورية
- فحص محافظ الحيتان
- تحليل السيولة
- دخول جماعي مع الحيتان
- + 26 اداة تانية

طرق الدفع:
1. فودافون كاش: 01050149684
2. انستا باي: 01050149684
3. USDT TRC20: كلمني ابعتهولك

📸 بعد الدفع ابعت سكرين التحويل هنا
⚡ التفعيل خلال 5 دقايق

للاستفسار: 01050149684
""")

# ========== امر تفعيل VIP ==========
@bot.message_handler(commands=['activate'])
def activate(message):
    if f"@{message.from_user.username}" not in VIP_USERS:
        bot.reply_to(message, "❌ الامر ده للادمن فقط")
        return
    try:
        username = message.text.split()[1]
        if username not in VIP_USERS:
            VIP_USERS.append(username)
        bot.reply_to(message, f"✅ تم تفعيل {username} بنجاح لمدة 30 يوم")
        bot.send_message(username, """
🎉 مبروك! تم تفعيل اشتراكك VIP

✅ كل الادوات مفتوحة دلوقتي
✅ تقدر تستخدم الـ 36 اداة

دوس /start وجرب 💎
""")
    except:
        bot.reply_to(message, "❌ الاستخدام الصح:\n/activate @username")

# ========== قفل باقي الادوات ==========
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text.startswith('/') or message.text in FREE_TOOLS or 'الاشتراك' in message.text:
        return

    if not check_vip(message.from_user):
        bot.reply_to(message, f"""
🔒 '{message.text}'
للمشتركين VIP فقط

💎 الادوات المجانية المتاحة:
1. الاسعار اللحظية
2. الاخبار العاجلة
3. التقويم الاقتصادي
4. من نحن
5. الدعم الفني

💰 للاشتراك وفتح كل الادوات:
دوس: الاشتراك الشهري

للاستفسار: 01050149684
""", reply_markup=main_keyboard())
    else:
        bot.reply_to(message, f"✅ جاري تجهيز '{message.text}'...\nهتكون متاحة خلال 24 ساعة 🔥")

@app.route('/')
def home():
    return "Siaf Bot Running ✅"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()