#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import argparse
import sys

from telegram.ext import Updater

import command
import data_base

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(stream=sys.stdout)]
)

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="TodoGit bot server.")
    parser.add_argument("-t", "--token-file",
                        help="Path to the text file with telegram token.", default="telegram.token")
    return parser.parse_args()


def get_telegram_token(file_name):
    file = open(file_name, "r")
    return file.readline().strip()

def main():
    """Start the bot."""

    print("Press Ctrl-C on the command line or send a signal to the process to stop the bot.")

    args = parse_args()
    token = get_telegram_token(args.token_file)
    updater = Updater(token, use_context=True)
    with data_base.session_scope() as session:
        command.add_commands(updater.dispatcher, session)
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    main()
