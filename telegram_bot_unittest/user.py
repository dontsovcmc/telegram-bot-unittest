from typing import Dict
from telegram import User, Chat

CHAT_ID = 1
BOT_ID = 5000000000
BOT_TOKEN = f'5000000000:BBFJVn-zqLnqQGv_Vrg75aJ5rqppy410rm0'


user = User(
    CHAT_ID,  # id
    'FN',  # first_name
    False,  # is_bot
    'LN',  # last_name
    'user1',  # username
    'ru')  # language_code

virtual_bot = User(
    BOT_ID,
    'PythonTelegramUnitTestBot',  # first_name
    True,  # is_bot
    None,  # last_name
    'PTUTestBot',  # username
    None,  # language_code
    True,  # can_join_groups
    False,  # can_read_all_group_messages
    False  # supports_inline_queries
)

chat = Chat(
    CHAT_ID,
    'private',  # type
    None,  # title
    'user1',  # username
    'FN',  # first_name
    'LN',  # last_name
)


class Client:

    def __init__(self, core):
        self.chat_id = CHAT_ID
        self.core = core
        self.core.init_queue(self.chat_id)

    def send_message(self, text: str) -> None:

        self.core.user_send(virtual_bot.id,
                            user_from=user.to_dict(),
                            chat=chat.to_dict(),
                            text=text
                            )

    def send_command(self, command: str) -> None:

        self.core.user_send_command(virtual_bot.id,
                                    user_from=user.to_dict(),
                                    chat=chat.to_dict(),
                                    command=command
                                    )

    def get_message(self, timeout=2.0) -> Dict:
        messages = self.core.get_updates(self.chat_id, timeout)
        if messages:
            return messages[0]['message']
