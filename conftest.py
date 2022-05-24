
import pytest
from _pytest.main import Session


@pytest.hookimpl()
def pytest_sessionstart(session: Session) -> None:

    print("Start pytest testing")


# Load fixtures
pytest_plugins = [
    'telegram_bot_unittest.fixtures',
    'telegram_bot_unittest.pytest.fixtures'

    #'examples.echobot.fixtures',
    #'examples.filebot.fixtures'
]
