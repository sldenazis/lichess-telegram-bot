import lichess.api
import re
import requests
import json

from telegram import Update, Bot
from telegram.ext import ContextTypes


async def puzzles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Save current solution to JSON, retrieve and update the following day
    #filename = 'oldPuzzle.json'

    response = requests.get('https://lichess.org/api/puzzle/daily')
    game = response.json()

    #solution = ['__' + move[0:2] + '➙' + move[2:] + '__' if index % 2 == 0 else move[0:2] + '➙' + move[2:]
    #        for index, move in enumerate(game['puzzle']['solution'])]

    print(game)
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

    #try:
    #    update_old_puzzle(bot, chat)
    #except Exception as e:
    #    print(e)

    #solution = ['__' + move[0:2] + '➙' + move[2:] + '__' if index % 2 == 0 else move[0:2] + '➙' + move[2:]
    #        for index, move in enumerate(game['puzzle']['solution'])]
    #themes = [f'#{theme.replace(" ", "_")}' for theme in game['puzzle']['themes']]
    #solution_str = f'{"".join(themes)}\n||{" ".join(solution)}||'

    #with open(filename, 'w') as f:
#        data = {'id': id, 'solution': solution_str, 'caption': caption}
#        f.write(json.dumps(data))

#def update_old_puzzle(bot, chat):
#    with open(filename, 'r') as f:
#        data = json.load(f)
#    message_id = data.get('id', -1)
#    if message_id == -1:
#        return
#    solution = data['solution']
#    caption = data['caption']
#    bot.edit_message_caption(chat_id=chat, message_id=message_id, caption=re.escape(f'{caption}\n{solution}'),
#                              parse_mode='MarkdownV2')

#send_puzzle_gif(game)

