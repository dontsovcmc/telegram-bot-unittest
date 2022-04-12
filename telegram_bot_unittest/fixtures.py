
import pytest
from .routes import start_server, shutdown_server
from .user import Client
from .core import core


@pytest.fixture(scope='session')
def user() -> Client:
    user = Client(core)
    return user


@pytest.fixture(scope='session')
def telegram_server():
    s, t = start_server()
    yield
    shutdown_server(s, t)
