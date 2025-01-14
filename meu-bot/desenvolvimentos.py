import os
import requests
from dotenv import load_dotenv
from gtts import gTTS
import google.generativeai as genai
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

# load_dotenv()

# TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")
# CHAT_GROUP_ID = os.getenv("CHAT_GROUP_ID")
# TOKEN_API = os.getenv("TOKEN_API")
# SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
# API_KEY = os.getenv("API_KEY")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TARGET_CHAT_ID="473291277"
CHAT_GROUP_ID="-4702645624"
TOKEN_API="7202685559:AAHa-HO0Th7WMkh5fHYa_OcC4njq86oQid0"
SEARCH_ENGINE_ID="f51791f34c66f4439"
API_KEY="AIzaSyBrfElqIdC1N-VhawMYDfOxqfRS54HU3c8"
GEMINI_API_KEY="AIzaSyA4sN6DC8ssBsFgQULCxXbZjpB5AMALXMQ"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

translator = GoogleTranslator(source="en", target="pt")

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
    mensagem = update.message.text.lower()

    if mensagem == "manda oi pro rafael":
        await update.message.reply_text(
            f"Oi, [Rafael](tg://user?id=5704397075)! Como é que você está?",
            parse_mode=ParseMode.MARKDOWN
        )

    if mensagem == "manda aquele oi pro rafael":
        print("procurando o audio")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        arquivo_audio = os.path.join(current_dir, "media", "oi_rafael.mp3")

        if os.path.exists(arquivo_audio):
            with open(arquivo_audio, 'rb'):
                await update.message.reply_audio(arquivo_audio)
        else:
            await update.message.reply_text("Estamos enfrendando alguns problemas em nossos servidores. Logo logo essa funcionalidade retornará ao nosso BOT.")

async def gemini_response(update: Update, context: CallbackContext) -> None:
    user_text = " ".join(context.args)

    if not user_text:
        await update.message.reply_text("Por favor, forneça uma consulta para a pesquisa.")
        return

    response = model.generate_content(user_text)

    text = response.text
    translated = translator.translate(text)
    await update.message.reply_text(translated)

async def send_audio(update: Update, context: CallbackContext) -> None:
    text = " ".join(context.args)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tts = gTTS(text, lang='pt')

    audio_path = os.path.join(current_dir, "media", "audio.mp3")
    tts.save(audio_path)

    if os.path.exists(audio_path):
        with open(audio_path, 'rb'):
            await update.message.reply_audio(audio_path)
    else:
        await update.message.reply_text("Estamos enfrendando alguns problemas em nossos servidores. Logo logo essa funcionalidade retornará ao nosso BOT.")


app = ApplicationBuilder().token(TOKEN_API).build()
app.add_handler(CommandHandler("members", get_group_members))
app.add_handler(CommandHandler("chatid", get_group_id))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_message))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("gemini", gemini_response))
app.add_handler(CommandHandler("audio", send_audio))

if __name__ == "__main__":
    app.run_polling()