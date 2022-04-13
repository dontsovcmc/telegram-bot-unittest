from typing import List, Dict
from datetime import datetime
from queue import Empty, Queue


# online telegram-bot-sdk
# https://telegram-bot-sdk.readme.io/reference/getupdates


epoch = datetime.utcfromtimestamp(0)


def now() -> int:
    return int((datetime.utcnow() - epoch).total_seconds())


def result_ok(result: List, ok: bool = True) -> Dict:
    return {
            "ok": ok,
            "result": result
    }


class TelegramCore:

    def __init__(self):
        self._message_counter = 0
        self._update_counter = 0
        self.income = {}

    def init_queue(self, id) -> None:
        if id not in self.income:
            self.income[id] = Queue()

    def user_send(self, bot_id, user_from, chat, text) -> Dict:

        self._message_counter += 1
        message = {'message_id': self._message_counter,
                   'from': user_from,
                   'chat': chat,
                   'date': now(),
                   'text': text
                   }

        self.init_queue(bot_id)
        self.income[bot_id].put(message)
        return message

    def user_send_command(self, bot_id: int, user_from, chat, command) -> None:

        self._message_counter += 1
        message = {'message_id': self._message_counter,
                   'from': user_from,
                   'chat': chat,
                   'date': now(),
                   'text': command,
                   "entities": [
                       {
                           "offset": 0,
                           "length": len(command),  # TODO ?
                           "type": "bot_command"
                       }]
                   }

        self.init_queue(bot_id)
        self.income[bot_id].put(message)

    def bot_send(self, bot_from, chat, text) -> Dict:

        self._message_counter += 1
        message = {'message_id': self._message_counter,
                   'from': bot_from,
                   'chat': chat,
                   'date': now(),
                   'text': text}

        self.init_queue(chat['id'])
        self.income[chat['id']].put(message)
        return message

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


core = TelegramCore()