
import pytest
from .routes import start_server, shutdown_server
from .user import Tester, UserBase, ChatBase
from .core import core


u = UserBase()
chat = ChatBase()


@pytest.fixture(scope='session')
def user() -> Tester:
    user = Tester(core, u, chat)
    return user


@pytest.fixture(scope='session')
def telegram_server():
    s, t = start_server()
    yield
    shutdown_server(s, t)
