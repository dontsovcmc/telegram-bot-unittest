Unit-tests for `python-telegram-bot <https://github.com/python-telegram-bot/python-telegram-bot>`_.

====================
How it works
====================

**This is a first version of library**

**Only long polling mode supported!**

Library starts your python-telegram-bot object with custom url (our unit-test server on Flask running under waitress).
Now you can communicate in unit-tests with your bot as you do in Telegram.


Features
-------------------

1. send text message
2. send command
3. send file
4. receive file


Fixtures
-------------------

user
--------------------------

User object to send messages and check incoming messages from your bot

bot
--------------------------
Your bot object. See 'Using'



Echo Bot example
--------------------------

Check echo of Echo Bot from python-telegram-bot example.

.. code::

    def test_echobot_message(bot, user):
        user.send_message('testing message')
        message = user.get_message()
        assert message['text'] == 'testing message'


Check /start command of Echo Bot

.. code::

    def test_echobot_start(bot, user):
        user.send_command('/start')
        message = user.get_message()
        assert message['text'] == 'Hi [FN LN](tg://user?id=1)\!'


File Bot example
---------------------------

Bot renames file you send to him.

.. code::

    def test_echobot_file(bot, user):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        user.send_document(current_dir, 'test.txt')

        document = user.get_document()

        file_io = document.path_or_bytes
        assert file_io.name == 'echo_test.txt'

        content = io.TextIOWrapper(file_io, encoding='utf-8').read()
        assert content == 'Hello world!\nHello world!'

==========
Installing
==========

You can install or upgrade telegram-bot-unittest with:

.. code::

    $ pip install telegram-bot-unittest --upgrade

Or you can install from source with:

.. code::

    $ git clone https://github.com/dontsovcmc/telegram-bot-unittest --recursive
    $ cd telegram-bot-unittest
    $ python setup.py install

====================
Using
====================

1. Create non-bloking function 'setup_bot' that runs your bot.
We need to separate updater.idle() and creating Updater().

.. code::

    def setup_bot(bot_token: str, base_url: str = None) -> Updater:

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


2. Add fixture 'bot' to you fixture.py file. Example:

.. code::

    import pytest
    from <your module> import <start_bot_function>
    from telegram_bot_unittest.routes import TELEGRAM_URL
    from telegram_bot_unittest.user import BOT_TOKEN

    @pytest.fixture(scope='session')
    def bot(telegram_server):
        updater = start_bot_function(BOT_TOKEN, TELEGRAM_URL)
        yield updater.bot
        updater.stop()


3. add 'telegram_bot_unittest.fixtures' to 'pytest_plugins' list in conftest.py

4. Add fixture 'bot' to you test functions.

5. Enjoy!

============
Contributing
============

Contributions of all sizes are welcome.

=======
License
=======

You may copy, distribute and modify the software provided that modifications are described and licensed for free under `LGPL-3 <https://www.gnu.org/licenses/lgpl-3.0.html>`_. Derivatives works (including modifications or anything statically linked to the library) can only be redistributed under LGPL-3, but applications that use the library don't have to be.
