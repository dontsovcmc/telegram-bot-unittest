
import pytest
from examples.filebot.filebot import setup_bot
from telegram_bot_unittest.routes import TELEGRAM_URL
from telegram_bot_unittest.user import BOT_TOKEN


@pytest.fixture(scope='session')
def bot(telegram_server):
    updater = setup_bot(BOT_TOKEN, TELEGRAM_URL)
    yield updater.bot
    updater.stop()
