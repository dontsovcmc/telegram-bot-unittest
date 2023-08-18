
import pytest

#from examples.echobot.echobot import setup_bot
from telegram_bot_unittest.pytest.testbot import setup_bot

from telegram_bot_unittest.routes import TELEGRAM_URL
from telegram_bot_unittest.user import BOT_TOKEN, CHAT_ID


@pytest.fixture(scope='session')
def bot(telegram_server):
    updater = setup_bot(BOT_TOKEN, TELEGRAM_URL)
    yield updater.bot
    updater.stop()


from telegram_bot_unittest.user import Tester, UserBase, ChatBase
from telegram_bot_unittest.core import core

user2_id = CHAT_ID+1

u2 = UserBase(user2_id)
chat2 = ChatBase(u2)


@pytest.fixture(scope='session')
def user2() -> Tester:
    user2 = Tester(core, u2, chat2)
    return user2
