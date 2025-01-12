from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
import requests

TARGET_CHAT_ID = "473291277"
CHAT_GROUP_ID = "-4702645624"
TOKEN_API = "7202685559:AAHa-HO0Th7WMkh5fHYa_OcC4njq86oQid0"
SEARCH_ENGINE_ID = "f51791f34c66f4439"
API_KEY = "AIzaSyBrfElqIdC1N-VhawMYDfOxqfRS54HU3c8"

def search_google(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"

    response = requests.get(url)

    if response.status_code == 200:
        results = response.json().get('items', [])
        return [(result['title'], result['link']) for result in results]
    else:
        return ["Erro na pesquisa"]

async def search(update: Update, context: CallbackContext):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Por favor, forneça uma consulta para a pesquisa.")
        return
    
    results = search_google(query)
    if results:
        response = "\n\n".join([f"{title}: {link}" for title, link in results[:5]])
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("Não encontrei resultados para a sua pesquisa.")

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

async def soma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Digite o primeiro número: ")
    numero = update.message.text

app = ApplicationBuilder().token(TOKEN_API).build()
app.add_handler(CommandHandler("members", get_group_members))
app.add_handler(CommandHandler("chatid", get_group_id))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_message))
app.add_handler(CommandHandler("soma", soma))
app.add_handler(CommandHandler("search", search))

if __name__ == "__main__":
    app.run_polling()