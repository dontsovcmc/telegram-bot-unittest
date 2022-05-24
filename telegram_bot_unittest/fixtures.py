
import pytest
import logging

from .routes import start_server, shutdown_server
from .user import Tester, UserBase, ChatBase
from .core import core

logger = logging.getLogger(__name__)


u = UserBase()
chat = ChatBase(u)


@pytest.fixture(scope='session')
def user() -> Tester:
    user = Tester(core, u, chat)
    return user


@pytest.fixture(scope='session')
def telegram_server():
    s, t = start_server()
    logger.info('telegram server started')
    yield
    core.print_queues()
    logger.info('telegram server shutdown begin')
    shutdown_server(s, t)
