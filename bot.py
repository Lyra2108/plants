import logging
import re
from uuid import uuid4

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler

import config
from api.plant import get_humidity, Plants


def plant_response(bot, update):
    plant_number = re.sub('^/plant ', '', update.message.text)
    if plant_number.isdigit():
        plants = Plants.get_plants(plant_number)
        if plants:
            humidity = get_humidity(plants[0].port)
            update.message.reply_text('The plants humidity is {0:.0f}%'.format(humidity))
            return

    keyboard = [[InlineKeyboardButton(plant.name, callback_data=plant.port) for plant in Plants.all()]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def selected_plant(bot, update):
    query = update.callback_query
    bot.edit_message_text(text='The plants humidity is {0:.0f}%'.format(get_humidity(query.data)),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def inline_query(bot, update):
    query = update.inline_query.query
    results = [InlineQueryResultArticle(
        id=uuid4(),
        title=plant.name,
        input_message_content=InputTextMessageContent('{0} has a humidity of {1:.0f}%'.format(plant.name, get_humidity(plant.port))))
        for plant in Plants.get_plants(query)]

    update.inline_query.answer(results)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
updater = Updater(config.telegram_api)
updater.dispatcher.add_handler(CommandHandler('plant', plant_response))
updater.dispatcher.add_handler(CallbackQueryHandler(selected_plant))
updater.dispatcher.add_handler(InlineQueryHandler(inline_query))
updater.start_polling()
updater.idle()
