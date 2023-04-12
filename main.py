#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position

import logging
import asyncio
import os

from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

from database import *
from activity import *
from puzzles import *
from users import *
from tops import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="pong")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hey there")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

TOKEN = os.environ.get('TOKEN', 'changeme')

if __name__ == '__main__':
    database_initialize()

    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    ping_handler = CommandHandler('ping', ping)
    application.add_handler(ping_handler)

    register_handler = CommandHandler('register', register)
    application.add_handler(register_handler)

    stats_handler = CommandHandler('stats', stats)
    application.add_handler(stats_handler)

    top_chat_handler = CommandHandler('top_chat', top_chat)
    application.add_handler(top_chat_handler)

    puzzles_handler = CommandHandler('puzzle', puzzles)
    application.add_handler(puzzles_handler)

    activity_handler = CommandHandler('activity', activity)
    application.add_handler(activity_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
