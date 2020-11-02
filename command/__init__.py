from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import ForceReply, ReplyKeyboardMarkup

import logging

from note import Note

logger = logging.getLogger(__name__)
_db_session = None

reply_keyboard = [
        ["add_note"],
        ["done"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)



CHOOSING, ADD_NOTE, TYPING_REPLY = range(3)

def add_commands(dispatcher, session):
    _db_session = session
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    conv_handler = ConversationHandler(
            entry_points=[CommandHandler("note", note)],
            states={
                CHOOSING: [
                    MessageHandler(Filters.regex("^add_note$"), add_note)
                ],
                TYPING_REPLY: [
                    MessageHandler(Filters.text & ~Filters.command, add_note_to_db)
                ]

            },
            fallbacks = [MessageHandler(Filters.regex('^Done$'), done)]
    )
    dispatcher.add_handler(conv_handler)

def done(update, context):
    update.message.reply_text("see you soon")
    return ConversationHandler.END

def note(update, context):
    """Begin converstion about your notes"""
    update.message.reply_text("Hello, what do you want?",
                                reply_markup = markup
                             )
    return CHOOSING

def add_note(update, context):
    """Create new note in db."""
    update.message.reply_text("pls enter you note", reply_markup=ForceReply())
    return TYPING_REPLY

def add_note_to_db(update,context):
    text = update.message.text
    # TODO create note here and insert it to db
    update.message.reply_text("you want"+"to remember:"+text)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    logger.info("user message: {message}".format(message=update.message.text))




