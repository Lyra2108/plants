import re

from telegram.ext import Updater, CommandHandler

import config
from api.plant import get_humidity


def plant(bot, update):
    plant_number = re.sub('^/plant','', update.message.text)
    humidity =  get_humidity(plant_number)
    update.message.reply_text('The plants humidity is {0:.0f}%'.format(humidity))


updater = Updater(config.telegram_api)
updater.dispatcher.add_handler(CommandHandler('plant', plant))
updater.start_polling()
updater.idle()
