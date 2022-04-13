from typing import Dict
from telegram import User, Chat

BOT_ID = 5000000000

BOT_TOKEN = f'5000000000:BBFJVn-zqLnqQGv_Vrg75aJ5rqppy410rm0'

CHAT_ID = 1


class UserBase(User):

    def __init__(self, id: int = CHAT_ID):
        super().__init__(
            id,  # id
            'FN',  # first_name
            False,  # is_bot
            'LN',  # last_name
            'user1',  # username
            'ru'  # language_code
        )


class ChatBase(Chat):

    def __init__(self, id: int = CHAT_ID):
        super().__init__(
            id,
            'private',  # type
            None,  # title
            'user1',  # username
            'FN',  # first_name
            'LN',  # last_name
        )


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


class Tester:

    def __init__(self, core, user, chat):
        self.core = core
        self.user = user
        self.chat = chat

    def send_message(self, text: str) -> None:

        self.core.user_send(virtual_bot.id,
                            user_from=self.user.to_dict(),
                            chat=self.chat.to_dict(),
                            text=text
                            )

    def send_command(self, command: str) -> None:

        self.core.user_send_command(virtual_bot.id,
                                    user_from=self.user.to_dict(),
                                    chat=self.chat.to_dict(),
                                    command=command
                                    )

    def get_message(self, timeout=2.0) -> Dict:
        messages = self.core.get_updates(self.user.id, timeout)
        if messages:
            return messages[0]['message']
