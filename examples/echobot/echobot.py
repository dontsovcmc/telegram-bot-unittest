import os

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


BOT_TOKEN = os.getenv("BOT_TOKEN")


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def setup_bot(bot_token: str, base_url: str = None) -> Updater:
    """Start the bot."""

    updater = Updater(bot_token, base_url=base_url)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    return updater


def main(base_url: str = None) -> None:

    updater = setup_bot(BOT_TOKEN, base_url)

    updater.idle()


if __name__ == '__main__':
    main()
