import lichess.api
from telegram import Update
from telegram.ext import ContextTypes

async def activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.args[0]

    activity = lichess.api.user_activity(username)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=activity)
