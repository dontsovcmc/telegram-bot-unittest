import os
import logging
import time
from io import BytesIO
from typing import Dict, List
from telegram import User, Chat, Contact
from .storage import DocumentBase, storage
from .core import TelegramCore

logger = logging.getLogger(__file__)


BOT_ID = 5000000000

BOT_TOKEN = f'5000000000:BBFJVn-zqLnqQGv_Vrg75aJ5rqppy410rm0'

CHAT_ID = 1


class ContactBase(Contact):

    def __init__(self, user, phone: str = '79991112233'):
        logger.debug(f'create ContactBase={user} with phone={phone}')
        super().__init__(
            phone,
            user.first_name,
            user.last_name,
            user.id
        )


class UserBase(User):

    def __init__(self, id: int = CHAT_ID):
        logger.debug(f'create UserBase={id}')
        super().__init__(
            id,  # id
            'FirstName',  # first_name
            False,  # is_bot
            'LastName',  # last_name
            f'user{id}',  # username
            'ru'  # language_code
        )


class ChatBase(Chat):

    def __init__(self, user: UserBase):
        logger.debug(f'create ChatBase={id}')
        super().__init__(
            user.id,
            'private',  # type
            None,  # title
            user.username,
            user.first_name,
            user.last_name,
        )


class BotBase(User):

    def __init__(self,
                 id: int = BOT_ID,
                 first_name='PythonTelegramUnitTestBot',
                 username='PTUTestBot'):

        logger.debug(f'create BotBase={id}')

        super().__init__(
            id,  # id
            first_name,
            True,  # is_bot
            None,  # last_name
            username,
            None,  # language_code
            True,  # can_join_groups
            False,  # can_read_all_group_messages
            False  # supports_inline_queries
        )


virtual_bot = BotBase()

chat = ChatBase(virtual_bot)


class LessMessages(Exception):
    pass


class Tester:

    def __init__(self, core: TelegramCore, user, chat, contact: ContactBase = None):
        self.core = core
        self.user = user
        self.chat = chat
        self.contact = contact if contact else ContactBase(user)

    @property
    def id(self):
        return self.user.id

    def clean_dialog(self):
        while self.get_message(timeout=0.5):
            pass

    def send_message(self, text: str) -> None:

        self.core.send(virtual_bot.id,
                       sender=self.user.to_dict(),
                       chat=self.chat.to_dict(),
                       text=text
                       )

    def send_command(self, command: str) -> None:

        self.core.send_command(virtual_bot.id,
                               sender=self.user.to_dict(),
                               chat=self.chat.to_dict(),
                               command=command
                               )

    def send_contact(self) -> None:
        self.core.send(virtual_bot.id,
                       sender=self.user.to_dict(),
                       chat=self.chat.to_dict(),
                       contact=self.contact.to_dict())

    def get_messages(self, count=1, timeout=2.0) -> List[Dict]:
        messages = []
        start = time.time()
        while len(messages) < count and time.time() - start < timeout:
            messages.extend(self.core.get_updates(self.user.id, timeout))

        if len(messages) != count:
            if not messages:
                raise LessMessages(f"No message received")
            raise LessMessages(f"Received {len(messages)} messages. Wait {count}")
        return [m['message'] for m in messages]

    def get_message(self, timeout=5.0) -> Dict:
        return self.get_messages(1, timeout)[0]

    def get_message_text(self, timeout=5.0) -> str:
        return self.get_messages(1, timeout)[0]['text']

    def send_document(self, dir: str, file_name: str) -> None:

        document = DocumentBase(dir, file_name)
        storage.add(document['file_id'], document)

        self.core.send(virtual_bot.id,
                       sender=self.user.to_dict(),
                       chat=self.chat.to_dict(),
                       document=document.to_dict()
                       )

    def get_document(self, timeout=5.0) -> BytesIO:
        message = self.get_message(timeout)
        assert 'document' in message, 'Message hasn\'t a file'

        file_id = message['document']['file_id']
        return storage.get(file_id)

    def assert_message(self, error_message: str):
        try:
            self.get_messages(1)
        except LessMessages:
            return
        raise Exception(error_message)

    def assert_get_keyboard(self, text: str, keyboard_text: str, request_contact: bool = True):
        """
        {'chat_id': 47390523,
         'text': "sometext",
         'reply_markup': '{"selective": false,
                           "keyboard": [[{"text": "Share contact", "request_contact": true}]],
                           "one_time_keyboard": true,
                           "resize_keyboard": true
                           }'
        }
        :return:
        """
        message = self.get_message()
        assert text in message['text'], 'Incorrect text: ' + message['text']
        assert 'reply_markup' not in message, 'No reply_markup found'

        #TODO понять, что бот шлет, что нет ответа
        #assert 'keyboard' not in message['reply_markup'], 'No keyboard found'
        #keyboard = message['reply_markup']['keyboard']
        #assert keyboard_text in keyboard['text'], 'Incorrect keyboard text: ' + keyboard['text']
        #assert request_contact == keyboard['request_contact'], 'Incorrect request_contact'
