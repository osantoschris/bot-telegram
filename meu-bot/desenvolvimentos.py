from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TARGET_CHAT_ID = "473291277"
CHAT_GROUP_ID = "-4702645624"
TOKEN_API = "7202685559:AAHa-HO0Th7WMkh5fHYa_OcC4njq86oQid0"

async def get_group_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("Este comando só funciona em grupos")
        return 

    chat = update.message.chat
    members = await context.bot.get_chat_administrators(chat.id)
    members_text = "Lista de membros do grupo\n"

    for member in members:
        user = member.user
        members_text += f"- {user.full_name} (ID: {user.id})\n"

    await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=members_text)

async def get_group_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=chat_id)

async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == "Manda oi pro rafael":
        await update.message.reply_text(
            f"Oi, [Rafael](tg://user?id=5704397075)! Como é que você está?",
            parse_mode=ParseMode.MARKDOWN
        )

app = ApplicationBuilder().token(TOKEN_API).build()
app.add_handler(CommandHandler("members", get_group_members))
app.add_handler(CommandHandler("chatid", get_group_id))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_message))

if __name__ == "__main__":
    app.run_polling()