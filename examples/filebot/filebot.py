
import os
import io

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


BOT_TOKEN = os.getenv("BOT_TOKEN")


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi!')


def echo_document(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    attachment = io.BytesIO()
    context.bot.get_file(update.message.document).download(out=attachment)
    attachment.seek(0)

    content = attachment.read().decode('utf-8')

    f = io.BytesIO(bytes(content, "utf-8"))
    f.name = 'echo_' + update.message.document.file_name
    f.seek(0)

    context.bot.send_document(chat_id, f)


def setup_bot(bot_token: str, base_url: str = None) -> Updater:
    """Start the bot."""
    updater = Updater(bot_token, base_url=base_url, base_file_url=base_url)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(MessageHandler(Filters.attachment, echo_document))

    updater.start_polling()

    return updater


def main(base_url: str = None) -> None:

    updater = setup_bot(BOT_TOKEN, base_url)
    updater.idle()


if __name__ == '__main__':
    main()
