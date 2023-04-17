import lichess.api
from telegram import Update
from telegram.ext import ContextTypes
from database import *
from helpers import *

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the Telegram user ID and the Lichess username from the message
    telegram_id = update.effective_user.id

    try:
        lichess_username = context.args[0]
    except Exception as error:
        print(f"Failed to register: {error}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Use /register yournick")
        return

    try:
        lichess_user = lichess.api.user(lichess_username)
    except Exception as error:
        print(f"Failed to retrieve user {lichess_username}: {error}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"User \"{lichess_username}\" doesn't exist, or Lichess is unavailable 🙃. Check if the username is correct and try again.")
        return

    register_query = f'INSERT OR REPLACE INTO users (telegram_id, lichess_username) VALUES ({telegram_id}, "{lichess_username}")'
    database_update(register_query)

    # Send a confirmation message
    message = f"Your Lichess username has been set to {lichess_username}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    if update.message.reply_to_message:
        telegram_id = update.message.reply_to_message.from_user.id

    stats_query = f'SELECT lichess_username FROM users WHERE telegram_id = {telegram_id}'
    result = database_fetchone(stats_query)

    if result is None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'You haven\'t registered your Lichess username yet. Use the /register command to register it')
        return

    lichess_username = result[0]

    try:
        lichess_user = lichess.api.user(lichess_username)
        perfs = lichess_user['perfs']

        md_username = md_escape_chars(lichess_username)

        message = []
        message.append(f"*Username:* [{md_username}]({lichess_user['url']})\n*Stats:*\n\n")

        for perf in perfs:
            if 'rating' in perfs[perf]:
                rating = f"{perfs[perf]['rating']}"

                if 'prov' in perfs[perf]:
                    if perfs[perf]['prov']:
                        rating += '?'

                r_message = f"▫️ *{perf}*: {rating}, *games played*: {perfs[perf]['games']}\n"
                message.append(r_message)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=''.join(message), parse_mode='MarkdownV2')
    except Exception as error:
        print(f"Failed to retrieve rating for user {lichess_username}: {error}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Failed to retrieve stats for user {lichess_username} 🙃")
