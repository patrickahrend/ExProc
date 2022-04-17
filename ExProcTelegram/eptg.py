# This script establishes the connect to Telegram. It handles sending and receiving of messages.
# Imports
import json
import logging
import os
import responses

from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from pathlib import Path

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
# URL = "https://api.telegram.org/bot{}/".format(TELEGRAM_TOKEN)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="eptg_logfile.txt",
    filemode="a+",
    level=logging.INFO,
)
command_dict = {}

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher


# Build in all functions here
def start(update, context):
    curr_command_list = [k for k, v in command_dict.items()]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="The following are currently acceptable commands:\n"
        + "\n".join(curr_command_list),
    )


def reboot_raspi(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Rebooting Raspi now."
    )
    os.system("sleep 5; sudo shutdown -r now")


def send_ep_logfile(update, context):
    context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=open(EP_Path / "ep_logfile.txt", "rb"),
    )
    context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=open(EP_Path / "eptg_logfile.txt", "rb"),
    )
    context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=open(EP_Path / "reboot_log.txt", "rb"),
    )


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Unrecognized command."
    )


# Message handler for interaction with the bot
def handle_message(update, context):
    text = str(update.message.text).lower()
    logging.info(f"User ({update.message.chat.id}) says: {text}")

    # Bot response
    response = responses.get_response(text)
    update.message.reply_text(response)


def shell_save_file(update, context):
    if context.args is None or update.message.document is None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Usage: /save_file <<save location with filename>> *Ensure file is attached to message.*",
        )
    elif len(context.args) > 1:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Args was too long."
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=" ".join(context.args)
        )


command_dict = {
    "/start": CommandHandler("start", start),
    "/reboot_raspi": CommandHandler("reboot_raspi", reboot_raspi),
    "/send_logs": CommandHandler("send_logs", send_ep_logfile),
    "/save_file": CommandHandler("save_file", shell_save_file, pass_args=True),
    "/send_message": MessageHandler(Filters.text, handle_message),
    "unknowncmd": MessageHandler(Filters.command, unknown),
}


for key, handler in command_dict.items():
    dispatcher.add_handler(handler)


# timeout is how long to keep a poll open before closing. poll_interval is how long to wait after the last poll.
updater.start_polling(1.0)
updater.idle()
