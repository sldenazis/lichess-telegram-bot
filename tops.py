import lichess.api
from telegram import Update
from telegram.ext import ContextTypes
from database import *

async def top_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # check if game mode is specified
    game_mode = 'classical'
    if len(context.args) > 0:
        game_mode = context.args[0].lower()

    users_query = "SELECT telegram_id, lichess_username FROM users"
    users = database_fetchall(users_query)

    if not users:
        update.message.reply_text("No users registered")
        return

    # retrieve the ratings of all users in current chat and create a dictionary
    ratings = {}
    for telegram_id, lichess_username in users:
        try:
            telegram_member = await context.bot.get_chat_member(update.message.chat_id, telegram_id)

            if telegram_member.status not in ['left', 'kicked']:
                lichess_user = lichess.api.user(lichess_username)
                rating = lichess_user['perfs'][game_mode]['rating']
                if rating is not None:
                    ratings[lichess_username] = rating

        except Exception as e:
            print(f"Failed to retrieve {game_mode} rating for user {lichess_username}: {e}")
            continue

    # sort the dictionary by rating and get the top 10
    top_10 = sorted(ratings.items(), key=lambda x: x[1], reverse=True)[:10]

    # format the response message
    response = ""
    for i, (lichess_username, rating) in enumerate(top_10):
        response += f"{i+1}. {lichess_username}: {rating}\n"

    if response == "":
        await context.bot.send_message(chat_id=update.effective_chat.id, text='No ratings found for the specified game mode.')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

