# This script establishes the connect to Telegram. It handles sending and receiving of messages.
# Imports
import json
import logging
import requests
import time
import urllib.parse

from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from pathlib import Path

from ExProcTelegram import eptg_responder as responder
# Some insight for later. All import should be understood as occurring from the main ExProc folder. Thus, even something imported from eptg.py needs to be imported as though from the root directory.


# Setup/Import of data, variables, paths
EP_Path = Path(__file__).parents[1]
datastore_folder = Path(EP_Path, "datastore")
telegram_folder = Path(EP_Path, "ExProcTelegram")

# Collecting some config variables
with open(datastore_folder / "ep_config.json", encoding="utf8") as datastore_auth:
    auth_json = json.load(datastore_auth)
    TELEGRAM_TOKEN = auth_json["api_keys"]["TELEGRAM_TOKEN"]

# Setting up other simple local variables
#URL = "https://api.telegram.org/bot{}/".format(TELEGRAM_TOKEN)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Build in all functions here
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
def reboot_raspi(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Rebooting Raspi now.")
    import os
    os.system('sleep 5; sudo shutdown -r now')


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

reboot_handler = CommandHandler('reboot_raspi', reboot_raspi)
dispatcher.add_handler(reboot_handler)

updater.start_polling()
