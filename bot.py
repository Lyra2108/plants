import logging
import re
from uuid import uuid4

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler

import config
from api.plant import get_humidity


def plant(bot, update):
    plant_number = re.sub('^/plant ', '', update.message.text)
    if plant_number.isdigit():
        humidity = get_humidity(plant_number)
        update.message.reply_text('The plants humidity is {0:.0f}%'.format(humidity))
    else:
        keyboard = [[InlineKeyboardButton("Minze", callback_data='10')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose:', reply_markup=reply_markup)


def selected_plant(bot, update):
    query = update.callback_query
    bot.edit_message_text(text='The plants humidity is {0:.0f}%'.format(get_humidity(query.data)),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def inline_query(bot, update):
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Minze",
            input_message_content=InputTextMessageContent(
                'Minze has a humidity of {0:.0f}%'.format(get_humidity(10))))]

    update.inline_query.answer(results)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
updater = Updater(config.telegram_api)
updater.dispatcher.add_handler(CommandHandler('plant', plant))
updater.dispatcher.add_handler(CallbackQueryHandler(selected_plant))
updater.dispatcher.add_handler(InlineQueryHandler(inline_query))
updater.start_polling()
updater.idle()
