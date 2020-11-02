from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import ForceReply, ReplyKeyboardMarkup

import logging

from note import Note

logger = logging.getLogger(__name__)

_db_session = None

reply_keyboard = [
        ["add_note"], ["show"],
        ["done"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)



CHOOSING, ADD_NOTE, TYPING_REPLY_NODE = range(3)

def add_commands(dispatcher, session):
    global _db_session
    _db_session = session
    conv_handler = ConversationHandler(
            entry_points=[CommandHandler("note", note)],
            states={
                CHOOSING: [
                    MessageHandler(Filters.regex("^add_note$"), add_note),
                    MessageHandler(Filters.regex("^show$"), show_notes)
                ],
                TYPING_REPLY_NODE: [
                    MessageHandler(Filters.text & ~Filters.command, add_note_to_db)
                ]

            },
            fallbacks = [MessageHandler(Filters.regex('^done$'), done)]
    )
    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

def done(update, context):
    update.message.reply_text("see you soon")
    return ConversationHandler.END

def note(update, context):
    """Begin converstion about your notes"""
    update.message.reply_text("Hello, what do you want?",
                                reply_markup = markup
                             )
    return CHOOSING


def show_notes(update,context):
    global _db_session
    assert _db_session is not None
    uid = update.effective_user.id
    result = _db_session.query(Note).all()
    update.message.reply_text("fuck", reply_markup = markup)
    print(result)
    return CHOOSING



def add_note(update, context):
    """Create new note in db."""
    update.message.reply_text("pls enter you note", reply_markup=ForceReply())
    return TYPING_REPLY_NODE

def add_note_to_db(update,context):
    global _db_session
    assert _db_session is not None
    text = update.message.text
    user_id = update.effective_user.id
    note = Note(user_id, text, 0)
    _db_session.add(note)
    update.message.reply_text("Node added: {}\n".format(text)+"What's next?",
                            reply_markup = markup) 
    return CHOOSING

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




