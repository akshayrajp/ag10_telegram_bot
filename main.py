import constants as C
import responses as R
import query as Q
from telegram.ext import *


# print a message to the console indicating that the bot has started running
print("Bot is currently running")


# handler definitions - start, user input (message) and error handlers.


def start_command(update, context):
    # send a nice little welcome message
    update.message.reply_text('Welcome to Team AG-10\'s Remote Monitoring Bot. Type help to get started!')


def handle_message(update, context):
    # convert text to lower case for easier handling
    text = str(update.message.text).lower()
    # send the message to responses(), which will in turn produce appropriate output based on the input
    response = R.responses(text)
    # send the output as a reply to the user
    update.message.reply_text(response)

def alert_message(update, context):
    # send alert message to the user
    update.message.reply_text(response)

def handle_error(update, context):
    # print error message to the console
    print(f"Update {update} caused error {context.error}")


def main():
    # create updaters and dispatcher using the token provided by BotFather
    updater = Updater(C.telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    # create a /start handler
    dispatcher.add_handler(CommandHandler("start", start_command))

    # handle user messages
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # handle alert messages
    dispatcher.add_handler(MessageHandler(Filters.text, alert_message))

    # handle errors and print them out to console
    dispatcher.add_error_handler(handle_error)

    # constantly check for messages,
    # and remain idle if there are no messages being receieved
    updater.start_polling()
    updater.idle()

    # alert messages
    while True:
        alertMessage = Q.alertMonitor()
        alert_message(alertMessage)


# start the process
main()
