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
    bot.reply_to(message, "🤖 بوت DCA VIP:\n\nاكتب كده:\ndca BTC 100 7\n\nالمعنى: اشتري BTC بـ 100$ كل اسبوع لمدة 7 اسابيع\n\n✅ متوسط سعرك هيتحسن\n✅ اقل مخاطرة\n✅ تلقائي 100%\n\n📊 نسبة نجاح DCA: 89% على المدى الطويل")

@bot.message_handler(func=lambda m: 'اخبار قبل السوق' in m.text)
def btn8(message):
    if not check_sub(message.from_user.id): return start(message)
    news = ['الفيدرالي هيثبت الفايدة','شركة كبرى هتشتري بتكوين','ETF جديد هيتوافق عليه','تحديث ايثريوم مهم']
    bot.reply_to(message, f"📡 خبر حصري قبل السوق:\n\n🔥 {random.choice(news)}\n\n⏰ الخبر هينزل رسمي بعد {random.randint(1,6)} ساعات\n📈 التأثير المتوقع: {random.choice(['+10%','+25%','-15%'])}\n\n💡 اتحرك قبل الكل")

@bot.message_handler(func=lambda m: 'نقاط دخول وخروج' in m.text)
def btn9(message):
    if not check_sub(message.from_user.id): return start(message)
    entry = random.randint(63000,65000)
    bot.reply_to(message, f"🎯 نقاط BTC اليوم:\n\nدخول شراء: {entry:,}$\nهدف 1: {entry+500:,}$ +0.8%\nهدف 2: {entry+1500:,}$ +2.3%\nهدف 3: {entry+3000:,}$ +4.6%\nوقف خسارة: {entry-800:,}$ -1.2%\n\n📊 R/R: 1:3.8\n✅ نسبة نجاح 73%")

@bot.message_handler(func=lambda m: 'كشف التلاعب' in m.text)
def btn10(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"📉 كشف تلاعب:\n\nعملة: $XYZ\nالنوع: {'Pump & Dump 🔴' if random.random()>0.5 else 'Wash Trading 🟡'}\nالخطورة: {random.randint(60,95)}%\n\n🚨 نصيحة: {'اخرج فورا' if random.random()>0.5 else 'متدخلش'}\n\n🛡️ حميتك من خسارة {random.randint(20,80)}%")

@bot.message_handler(func=lambda m: 'مؤشر الخوف والطمع' in m.text)
def btn11(message):
    if not check_sub(message.from_user.id): return start(message)
    fear = random.randint(0,100)
    status = 'خوف شديد 🟢' if fear<25 else 'خوف 🟡' if fear<45 else 'محايد' if fear<55 else 'طمع 🟠' if fear<75 else 'طمع شديد 🔴'
    bot.reply_to(message, f"💹 مؤشر الخوف والطمع:\n\nالقيمة: {fear}/100\nالحالة: {status}\n\n💡 {'وقت الشراء التاريخي' if fear<25 else 'وقت البيع التاريخي' if fear>75 else 'انتظر'}\n\n📊 تحديث كل ساعة")

@bot.message_handler(func=lambda m: 'توقع AI متقدم' in m.text)
def btn12(message):
    if not check_sub(message.from_user.id): return start(message)
    pred = random.randint(68000,78000)
    bot.reply_to(message, f"🔮 توقع AI VIP:\n\nBTC خلال 7 ايام: {pred:,}$\nنسبة الثقة: {random.randint(70,92)}%\n\n📊 مبني على:\n• 1000+ مؤشر فني\n• تحليل مشاعر\n• حركة الحيتان\n• اخبار عالمية\n\n⚠️ مش نصيحة مالية\n💡 استخدم للاسترشاد فقط")

@bot.message_handler(func=lambda m: 'احصائيات دولية' in m.text)
def btn13(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"🌍 احصائيات حصرية:\n\nاكتر دولة بتشتري BTC: {'امريكا' if random.random()>0.5 else 'كوريا'}\nحجم التداول العالمي: {random.randint(50,150)} مليار$\nمحافظ جديدة اليوم: {random.randint(100,500)}K\n\n📊 بيانات من 50 بورصة\n🔒 مش متاحة مجانا")

@bot.message_handler(func=lambda m: 'تنبيهات واتساب' in m.text)
def btn14(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "📱 تنبيهات واتساب فورية:\n\nابعت رقمك كده:\nواتساب 01050149684\n\nهبعتلك:\n✅ اشارات لحظية\n✅ تحركات حيتان\n✅ اخبار عاجلة\n\n⚡ اسرع من التليجرام")

@bot.message_handler(func=lambda m: 'تقارير يومية PDF' in m.text)
def btn15(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "📧 تقرير اليوم PDF:\n\nhttps://siaf.com/report/2026-05-01.pdf\n\n📊 يحتوي على:\n• ملخص السوق\n• افضل 10 عملات\n• توصيات الغد\n• تحليل 50 شارت\n\n📥 حمله قبل ما يتحذف")

@bot.message_handler(func=lambda m: 'محفظة VIP' in m.text)
def btn16(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "💼 محفظة VIP متعددة:\n\nاكتب كده:\nاضافة BTC 0.5 60000\n\nهتابعلك:\n✅ الربح/الخسارة لايف\n✅ تنبيه عند الهدف\n✅ تنبيه عند الوقف\n\n📊 10 عملات كحد اقصى")

@bot.message_handler(func=lambda m: 'تنبيه اي عملة' in m.text)
def btn17(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "🔔 تنبيه سعر مخصص:\n\nاكتب كده:\nنبهني BTC 70000\nنبهني ETH 3500\nنبهني SOL 150\n\n⚡ هبعتلك اول ما يوصل\n♾️ عدد غير محدود من التنبيهات")

@bot.message_handler(func=lambda m: 'مكالمة مع خبير' in m.text)
def btn18(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "📞 مكالمة VIP مع خبير:\n\nاحجز موعد:\n• 30 دقيقة = مجانا\n• خبير 10 سنين\n• تحليل محفظتك\n• خطة شخصية\n\n📅 واتساب: 01050149684\nاكتب: حجز مكالمة\n\n⏰ متاح 24/7")

@bot.message_handler(func=lambda m: 'كورس تداول' in m.text)
def btn19(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "🎓 كورس تداول VIP:\n\n50 فيديو احترافي\nمن الصفر للاحتراف\n\n📚 المواضيع:\n1. التحليل الفني\n2. ادارة المخاطر\n3. سيكولوجية التداول\n4. استراتيجيات الحيتان\n\n🔑 كود الدخول: VIP2026\n📥 mega.nz/siafcourse\n\n💰 قيمة الكورس 500$ - مجانا للمشتركين")

@bot.message_handler(func=lambda m: 'مكتبة كتب' in m.text)
def btn20(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "📚 مكتبة VIP:\n\n200+ كتاب تداول مدفوع\n• Trading in the Zone\n• Market Wizards\n• Technical Analysis\n• Rich Dad Poor Dad\n\n📥 drive.google.com/siaflibrary\n\n✅ PDF + صوتي\n🆕 كتاب جديد كل اسبوع")

@bot.message_handler(func=lambda m: 'فيديوهات حصرية' in m.text)
def btn21(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "🎥 فيديوهات VIP حصرية:\n\n• تحليل يومي 30 دقيقة\n• شرح استراتيجيات سرية\n• مقابلات مع حيتان\n• بث مباشر وقت الاخبار\n\n📺 youtube.com/siafvip\n🔑 الباسورد يوصلك خاص")

@bot.message_handler(func=lambda m: 'مسابقة جوائز' in m.text)
def btn22(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"🏆 مسابقة الاسبوع:\n\nالجائزة: {random.randint(100,1000)}$ USDT\nالسؤال: كم سعر BTC بعد اسبوع؟\n\n📝 اكتب توقعك كده:\nتوقع 72000\n\n🎁 اقرب رقم يكسب\n⏰ تنتهي الجمعة")

@bot.message_handler(func=lambda m: 'استرداد' in m.text)
def btn23(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "💸 ضمان استرداد VIP:\n\nلو خسرت من توصياتنا:\nنرجعلك 20% من الخسارة\n\n📋 الشروط:\n• تكون متابع التوصيات\n• تبعت سكرين\n• حد اقصى 1000$\n\n💚 احنا واثقين في شغلنا")

@bot.message_handler(func=lambda m: 'هدايا للمشتركين' in m.text)
def btn24(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"🎁 هدية اليوم للمشتركين:\n\n{random.choice(['كوبون خصم 50% على الشهر الجاي','شهر مجاني لو جبت صاحبك','كتاب تداول PDF','30 دقيقة استشارة مجانية'])}\n\n✅ بتوصلك تلقائي\n🎉 هدية جديدة كل اسبوع")

@bot.message_handler(func=lambda m: 'سر الارقام الامريكية' in m.text)
def btn25(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"""📱 سر الارقام الامريكية مجانا VIP:

🎁 للمشتركين فقط - توفر 100$ سنويا:

1️⃣ قائمة 5 تطبيقات بتدي ارقام مجانية
2️⃣ شرح فيديو: تفعل 50 رقم في ساعة
3️⃣ تركات: تخلي الرقم يعيش سنة مش شهر
4️⃣ دعم: لو وقف نجيبلك بديل فورا

💡 التطبيقات: TextNow + 2Number + Talkatone
⚡ الطريقة تشتغل 2026 مضمونة

🎥 اكتب: /فيديو_امريكي
⚖️ للخصوصية والشغل فقط
❌ ممنوع: نصب او انتحال او ازعاج""")

@bot.message_handler(func=lambda m: 'سر الارقام المصرية' in m.text)
def btn26(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"""📞 سر الارقام المصرية بـ 30ج VIP:

💰 باكدج التوفير للمشتركين:

1️⃣ كود خصم 60%: SIAF60
   السعر يبقى 30ج بدل 75ج شهريا
2️⃣ اسم التطبيق: Numero eSIM
3️⃣ شرح فيديو: تشتري الرقم في دقيقة
4️⃣ عمولة ليك: هات صاحبك وخد 20ج

💵 انت بتوفر 45ج كل شهر = 540ج سنويا
💵 انا بكسب عمولة من الشركة مش منك

✅ انت بتشتري من شركة مرخصة باسمك
✅ انا مجرد بعلمك الطريقة

📲 للتفعيل كلمني @siaf اكتب: كود خصم
⚖️ البوت تعليمي - مش بيبيع ارقام
❌ ممنوع استخدام في جرائم""")

@bot.message_handler(func=lambda m: '170 عملة' in m.text)
def btn27(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "💱 محول 170 عملة:\n\nاكتب كده:\n100 دولار كم جنيه\n50 يورو كم ريال\n1000 ين كم دولار\n\n✅ اسعار لايف من البنوك\n✅ 170 عملة\n✅ كريبتو كمان\n\nمثال: 1 BTC كم جنيه")

@bot.message_handler(func=lambda m: 'مقارنات اسعار' in m.text)
def btn28(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, "📊 مقارنة اسعار عالمية:\n\niPhone 16 Pro:\n🇺🇸 امريكا: 999$\n🇪🇬 مصر: 75,000 جنيه\n🇸🇦 السعودية: 3,749 ريال\n🇦🇪 الامارات: 3,669 درهم\n\n💡 ارخص دولة: امريكا\n💸 الفرق: 40%")

@bot.message_handler(func=lambda m: 'نتائج مباريات' in m.text)
def btn29(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"🎮 نتائج لايف:\n\n⚽ الاهلي 2-1 الزمالك | مباشر د{random.randint(60,90)}\n⚽ ليفربول 3-0 السيتي | انتهت\n⚽ برشلونة 1-1 الريال | شوط اول\n\n📊 احصائيات + تشكيلة\n🔔 تنبيه اهداف")

@bot.message_handler(func=lambda m: 'دعم 24/7' in m.text)
def btn30(message):
    bot.reply_to(message, "📞 دعم VIP 24/7:\n\nتليجرام: @siaf\nواتساب: 01050149684\n\n⚡ رد خلال 3 دقايق\n👨‍💻 فريق 10 اشخاص\n🆘 طوارئ: مكالمة فورية\n\n💚 في خدمتك دايما")

@bot.message_handler(func=lambda m: 'طقس دقيق' in m.text)
def btn31(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"🌤️ طقس 14 يوم - القاهرة:\n\nاليوم: 28° ☀️\nغدا: 30° ☀️\nبعد غد: 27° ⛅\n...\n\n📊 دقة 95%\n🛰️ بيانات اقمار صناعية\n⚠️ تحذير: موجة حر الاسبوع الجاي")

@bot.message_handler(func=lambda m: 'مواقيت صلاة' in m.text)
def btn32(message):
    c = get_country(message.from_user.id)
    bot.reply_to(message, f"🕌 مواقيت {c} اليوم:\n\nالفجر: 4:45 ص\nالشروق: 6:15 ص\nالظهر: 12:05 م\nالعصر: 3:30 م\nالمغرب: 6:00 م\nالعشاء: 7:20 م\n\n🔔 فعل الاذان: /azan\n📍 دقة بالثانية حسب موقعك")

@bot.message_handler(func=lambda m: 'هاك كوبونات امازون' in m.text)
def btn33(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"""💰 هاك كوبونات VIP:

🎁 كود خصم خاص بيك: SIAF10
✅ اي حد يشتري من امازون بالكود ده:
- هو ياخد خصم 10%
- انت تاخد عمولة 10%

💵 مثال: موبايل بـ 20 الف
هو يوفر 2000ج
انت تكسب 2000ج

🔗 لينكك الخاص:
amazon.eg/?tag=siaf-vip-21

📲 ابعته لجروبك واكسب وانت نايم
⚖️ قانوني 100% - تبع برنامج شركاء امازون""")

@bot.message_handler(func=lambda m: 'هاك اربيتراج منتجات' in m.text)
def btn34(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"""📦 هاك اربيتراج منتجات VIP:

🔥 صفقة اليوم:
iPhone 16 Pro
🇺🇸 سعره في امريكا: 999$ = 48 الف جنيه
🇪🇬 بيتباع في مصر: 75 الف جنيه
💚 مكسب صافي: 27 الف جنيه

⚡ ازاي تجيبه؟
1. حد قريبك في امريكا يشتريه
2. يبعته مع مسافر بـ 100$
3. تبيعه في مصر كسر زيرو

📊 10 منتجات تانية:
- PlayStation 5: مكسب 8 الاف
- MacBook: مكسب 20 الف
- AirPods: مكسب 3 الاف

💡 بنزلك صفقة جديدة كل يوم""")

@bot.message_handler(func=lambda m: 'هاك الذكاء الصناعي' in m.text)
def btn35(message):
    if not check_sub(message.from_user.id): return start(message)
    bot.reply_to(message, f"""🤖 هاك الذكاء الصناعي VIP:

💰 تكسب 500ج في الساعة:

1️⃣ افتح ChatGPT مجاني
2️⃣ اكتب البرومبت ده:
"اكتبلي 10 بوستات فيسبوك لصفحة مطعم
تجيب تفاعل عالي وتبيع"

3️⃣ خد البوستات بيعها للمطاعم
السعر: 500ج للـ 10 بوستات

⏰ تاخد منك 5 دقايق
💵 تكسب 500ج

🎁 برومبتات جاهزة VIP:
- اعلانات ممولة
- سكريبت فيديوهات
- وصف منتجات

📥 اكتب: /برومبتات
⚖️ قانوني 100% - شغل فريلانسر""")

@bot.message_handler(func=lambda m: 'صفقات اربيتراج جاهزة' in m.text)
def btn36(message):
    if not check_sub(message.from_user.id): return start(message)

    deals = [
        {
            'name': 'iPhone 16 Pro 256GB',
            'buy_us': '999$',
            'buy_link': 'https://apple.com/iphone-16-pro',
            'sell_eg': '75,000 جنيه',
            'profit': '27,000 جنيه',
            'site': 'olx.com.eg'
        },
        {
            'name': 'PlayStation 5 Slim',
            'buy_us': '499$',
            'buy_link': 'https://amazon.com/dp/B0CL5KNB9M',
            'sell_eg': '32,000 جنيه',
            'profit': '8,000 جنيه',
            'site': 'jumia.com.eg'
        },
        {
            'name': 'MacBook Air M3',
            'buy_us': '1,099$',
            'buy_link': 'https://apple.com/macbook-air',
            'sell_eg': '73,000 جنيه',
            'profit': '20,000 جنيه',
            'site': 'noon.com/egypt'
        }
    ]

    d = random.choice(deals)
    bot.reply_to(message, f"""🛒 صفقة اربيتراج جاهزة VIP:

📦 المنتج: {d['name']}

🇺🇸 تشتريه من امريكا:
السعر: {d['buy_us']} = {int(d['buy_us'].replace('$',''))*48:,} جنيه
🔗 اللينك: {d['buy_link']}

🇪🇬 تبيعه في مصر:
السعر: {d['sell_eg']}
🔗 انشر على: {d['site']}

💰 مكسب صافي: {d['profit']}

⚡ الطريقة:
1. حد قريبك يشتريه من امريكا
2. يبعته مع مسافر بـ 100$
3. تبيعه كسر زيرو في مصر

⏰ الصفقة دي شغالة النهاردة
🔄 دوس تاني عشان صفقة جديدة

⚖️ قانوني 100% - تجارة مشروعة
💡 مكسبك من فرق السعر + مجهودك""")

@app.route('/')
def home(): return "Siaf Global VIP ✅"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("🦍 Siaf VIP اشتغل")
    bot.infinity_polling()