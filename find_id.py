from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Seu ID é: {update.effective_user.id}")

async def show_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Seu ID é: {user_id}\nID do chat: {chat_id}")


BOT_TOKEN = "7484429897:AAH6VPGbA0zts0-NTTiOWe8NqLl1V4Rxwuo"

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, show_id))

if __name__ == "__main__":
    app.run_polling()