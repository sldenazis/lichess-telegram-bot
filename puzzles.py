import re
import requests
import json

from telegram import Update
from telegram.ext import ContextTypes


async def puzzles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get('https://lichess.org/api/puzzle/daily')
    game = response.json()

    color = 'Black' if game['puzzle']['initialPly'] % 2 == 0 else 'White'
    url = f'https://lichess.org/training/{game["puzzle"]["id"]}'
    caption = f'{color} to move\n{url}'
    gif_url = f'https://lichess1.org/training/export/gif/thumbnail/{game["puzzle"]["id"]}.gif'

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=gif_url,
        caption=re.escape(caption),
        parse_mode='MarkdownV2'
    )
