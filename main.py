import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime, timedelta

TOKEN =''8434129325:AAEWCXWll6QeuL9WwpMVFpJLAxNwP2gFcIc"
ADMIN_ID = 123456789 @siaf_btc_alert_bot

# قاعدة البيانات
conn = sqlite3.connect('siaf.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS subs
               (user_id INTEGER PRIMARY KEY, end_date TEXT)''')
conn.commit()

def add_sub(user_id):
    end = datetime.now() + timedelta(days=30)
    cursor.execute("INSERT OR REPLACE INTO subs VALUES (?,?)", (user_id, end.isoformat()))
    conn.commit()

def check_sub(user_id):
    cursor.execute("SELECT end_date FROM subs WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if row and datetime.fromisoformat(row[0]) > datetime.now():
        return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اهلا بيك في SIAF\n/start\n/subscribe\n/vip")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اشتراك VIP بـ 50 جنيه\nفودافون كاش: 01012345678\nبعد التحويل كلمنا")

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if check_sub(user_id):
        await update.message.reply_text("💎 انت VIP")
    else:
        await update.message.reply_text("🔒 اشترك الاول: /subscribe")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id!= ADMIN_ID: return
    keyboard = [
        [InlineKeyboardButton("✅ تفعيل VIP", callback_data='activate')],
        [InlineKeyboardButton("📊 الاحصائيات", callback_data='stats')]
    ]
    await update.message.reply_text("💎 لوحة التحكم", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id!= ADMIN_ID: return
    if query.data == 'activate':
        await query.edit_message_text("ابعت: /activate 123456789")
    elif query.data == 'stats':
        cursor.execute("SELECT COUNT(*) FROM subs WHERE end_date >?", (datetime.now().isoformat(),))
        active = cursor.fetchone()[0]
        await query.edit_message_text(f"المشتركين: {active}")

async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id!= ADMIN_ID: return
    try:
        user_id = int(context.args[0])
        add_sub(user_id)
        await update.message.reply_text(f"✅ اتفعل {user_id}")
        await context.bot.send_message(user_id, "🎉 اشتراكك VIP اتفعل 30 يوم")
    except:
        await update.message.reply_text("استخدم: /activate user_id")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("activate", activate))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("البوت شغال...")
    app.run_polling()

if __name__ == '__main__':
    main()