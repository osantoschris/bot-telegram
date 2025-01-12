import time, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# TARGET_CHAT_ID = "473291277"
TARGET_CHAT_ID = "5704397075"
BOT_TOKEN = "7484429897:AAH6VPGbA0zts0-NTTiOWe8NqLl1V4Rxwuo"

bot_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    bot_data[user_id] = {"text": None, "count": None}
    await update.message.reply_text("Olá! Envie o que deseja repetir.")

async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    if user_id in bot_data and bot_data[user_id]["text"] is None:
        bot_data[user_id]["text"] = update.message.text

        keyboard = [
            [InlineKeyboardButton("10", callback_data="10"), InlineKeyboardButton("20", callback_data="20")],
            [InlineKeyboardButton("30", callback_data="30"), InlineKeyboardButton("40", callback_data="40")],
            [InlineKeyboardButton("50", callback_data="50"), InlineKeyboardButton("100", callback_data="100")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Escolha a quantidade de vezes que deseja enviar a mensagem", reply_markup=reply_markup)

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id

    if user_id in bot_data and bot_data[user_id]["text"] is not None:
        count = int(query.data)
        bot_data[user_id]["count"] = count
        await query.message.reply_text(f"Enviando sua mensagem {count} vezes!")

        for _ in range(count):
            # time.sleep(random.randint(1, 10))
            await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=bot_data[user_id]["text"])
        
        bot_data[user_id] = {"text": None, "count": None}

async def receive_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    if user_id in bot_data and bot_data[user_id]["text"] is not None:
        try:
            count = int(update.message.text)
            bot_data[user_id]["count"] = count
            await update.message.reply_text(f"Enviando sua mensagem {count} vezes!")
            for _ in range(count):
                await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=bot_data[user_id]["text"])
            bot_data[user_id] = {"text": None, "count": None}
        except ValueError:
            await update.message.reply_text("Por favor, envie um número válido.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text))
app.add_handler(CallbackQueryHandler(handle_button_click))

if __name__ == "__main__":
    app.run_polling()