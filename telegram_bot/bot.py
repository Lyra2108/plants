import logging
import re
from gettext import gettext as _, translation
from uuid import uuid4

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler

from api.plant import get_humidity, Plants
from telegram_bot import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='log.txt')

trans = translation('messages', localedir='locales', languages=[config.language])
trans.install()
_ = trans.gettext


def plant_response(bot, update):
    plant_number = re.sub('^/plant *', '', update.message.text)
    if plant_number:
        plants = Plants.get_plants(plant_number)
        if plants:
            humidity = get_humidity(plants[0].port)
            update.message.reply_text(_("The plant's humidity is {0:.0f}%").format(humidity))
            return

    keyboard = [[InlineKeyboardButton(plant.name, callback_data=plant.port) for plant in Plants.all()]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(_('Please choose:'), reply_markup=reply_markup)


def selected_plant(bot, update):
    query = update.callback_query
    bot.edit_message_text(text=_("The plant's humidity is {0:.0f}%").format(get_humidity(query.data)),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def inline_query(bot, update):
    query = update.inline_query.query
    results = [InlineQueryResultArticle(
        id=uuid4(),
        title=plant.name,
        input_message_content=InputTextMessageContent(
            _('{0} has a humidity of {1:.0f}%').format(plant.name, get_humidity(plant.port))))
        for plant in Plants.get_plants(query)]

    update.inline_query.answer(results)


def main():
    updater = Updater(config.telegram_api)
    updater.dispatcher.add_handler(CommandHandler('plant', plant_response))
    updater.dispatcher.add_handler(CallbackQueryHandler(selected_plant))
    updater.dispatcher.add_handler(InlineQueryHandler(inline_query))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
