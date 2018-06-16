import logging
import re
from gettext import gettext as _, translation
from uuid import uuid4

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler

from api.plant import Plants
from telegram_bot import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

trans = translation('messages', localedir='locales', languages=[config.language])
trans.install()
_ = trans.gettext


def plant_response(bot, update):
    plant_number = re.sub('^/plant *', '', update.message.text)
    if plant_number:
        plants = Plants.get_plants(plant_number)
        if plants:
            plant = plants[0]
            update.message.reply_text(plant.get_humidity_display_text())
            return

    display_choose_keyboard(bot, update.message.chat_id)


def selected_plant(bot, update):
    query = update.callback_query
    plant = Plants.get_plant_by_id(query.data)
    bot.edit_message_text(text=plant.get_humidity_display_text(),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    display_choose_keyboard(bot, query.message.chat_id)


def plants_response(bot, update):
    plants = Plants.all()
    text = "```\n" + \
           "| {0:^15} | {1:^5} |\n".format(_("Plant"), "%") + \
           "|{0:-<17}|{0:-<7}|\n".format('') + \
           '\n'.join(['| {0:15.15} | {1:4.0f}% |'.format(plant.name, plant.get_humidity()) for plant in plants]) + \
           '```'
    update.message.reply_markdown(text)


def inline_query(bot, update):
    query = update.inline_query.query
    results = [InlineQueryResultArticle(
        id=uuid4(),
        title=plant.name,
        input_message_content=InputTextMessageContent(plant.get_humidity_display_text()))
        for plant in Plants.get_plants(query)]

    update.inline_query.answer(results)


def display_choose_keyboard(bot, chat_id):
    keyboard = [[InlineKeyboardButton(plant.name, callback_data=plant.id) for plant in Plants.all()]]
    bot.send_message(text=_('Please choose:'),
                     reply_markup=(InlineKeyboardMarkup(keyboard)),
                     chat_id=chat_id)


def main():
    updater = Updater(config.telegram_api)
    updater.dispatcher.add_handler(CommandHandler('plant', plant_response))
    updater.dispatcher.add_handler(CommandHandler('plants', plants_response))
    updater.dispatcher.add_handler(CallbackQueryHandler(selected_plant))
    updater.dispatcher.add_handler(InlineQueryHandler(inline_query))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
