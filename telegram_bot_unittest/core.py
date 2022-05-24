from typing import List, Dict
from datetime import datetime
from queue import Empty, Queue

from telegram.utils.types import JSONDict

import logging
logger = logging.getLogger(__name__)


# online telegram-bot-sdk
# https://telegram-bot-sdk.readme.io/reference/getupdates


epoch = datetime.utcfromtimestamp(0)


def now() -> int:
    return int((datetime.utcnow() - epoch).total_seconds())


class TelegramCore:

    def __init__(self):
        self._message_counter = 0
        self._update_counter = 0
        self.income = {}

    def init_queue(self, id: int) -> None:
        """
        Initialize message queue
        :param id: chat_id
        :return:
        """
        if isinstance(id, str):
            raise Exception('chat_id should be int')
        if id not in self.income:
            self.income[id] = Queue(100)

    def send(self, receiver_id: int, sender: JSONDict, chat: JSONDict, **kwargs) -> JSONDict:
        """
        Message from User to Bot
        :param receiver_id:
        :param sender:
        :param chat:
        :param kwargs: text, document, entities, contact
        :return:
        """
        self._message_counter += 1
        message = {'message_id': self._message_counter,
                   'from': sender,
                   'chat': chat,
                   'date': now()
                   }

        for i in kwargs.keys():
            message.update({i: kwargs.get(i)})

        self.init_queue(receiver_id)
        self.income[receiver_id].put(message, block=False)
        return message

    def send_command(self, bot_id: int, sender: JSONDict, chat: JSONDict, command: str) -> JSONDict:
        """
        Command message from User to Bot
        :param bot_id:
        :param sender:
        :param user_from:
        :param chat:
        :param command:
        :return:
        """
        entities = [
            {
                "offset": 0,
                "length": len(command),  # TODO ?
                "type": "bot_command"
            }
        ]
        return self.send(bot_id, sender, chat, text=command, entities=entities)

    def get_updates(self, chat_id: int, timeout: float = 2.0) -> List[Dict]:

        ret = []
        try:
            if chat_id not in self.income:
                self.init_queue(chat_id)

            message = self.income[chat_id].get(timeout=timeout)

            self._update_counter += 1
            ret = [{'update_id': self._update_counter,
                    'message': message
                    }]

        except Empty:
            pass

        return ret

    def print_queues(self):
        """
        Print messages in queue if exist when turn off.
        """
        for chat_id, queue in self.income.items():

            try:
                message = self.income[chat_id].get_nowait()

                out = f'chat_id: {chat_id}\n'

                while message:
                    try:
                        out += str(message) + '\n'
                        message = self.income[chat_id].get_nowait()
                    except Empty:
                        break

                if out:
                    logger.info(out)
            except Empty:
                pass


core = TelegramCore()