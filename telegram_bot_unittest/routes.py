import logging
import json
import threading
import waitress
from flask import Flask, request, make_response

from flask import json
from .core import result_ok, core
from .user import virtual_bot, chat

logger = logging.getLogger(__name__)

app = Flask(__name__)

HOST = '127.0.0.1'
PORT = 5555
TELEGRAM_URL = f'http://{HOST}:{PORT}/'


def server_response(data):

    r = make_response(
       json.dumps(result_ok(data)),
       200
    )
    r.headers['Content-Type'] = 'application/json'
    return r


@app.route('/<token>/getMe', methods=['POST'])
def getMe(token: str):
    j = request.get_json()  # cause flask bug

    bot_id = int(token.split(':')[0])

    core.init_queue(bot_id)

    ret = virtual_bot.to_dict()
    return server_response(ret)


@app.route('/<token>/deleteWebhook', methods=['POST'])
def deleteWebhook(token: str):
    j = request.get_json()  # cause flask bug
    return server_response(True)


@app.route('/<token>/getUpdates', methods=['POST'])
def getUpdates(token: str):
    j = request.get_json()  # cause flask bug

    bot_id = int(token.split(':')[0])

    ret = core.get_updates(bot_id)

    return server_response(ret)


@app.route('/<token>/sendMessage', methods=['POST'])
def sendMessage(token: str):

    #bot_id = int(token.split(':')[0])

    data = request.get_json()

    chat_id = int(data['chat_id'])
    text = data['text']

    ret = core.bot_send(bot_from=virtual_bot.to_dict(),
                        chat=chat.to_dict(),
                        text=text
                        )

    return server_response(ret)


def start_server():
    s = waitress.create_server(app, host=HOST, port=PORT)
    t = threading.Thread(target=s.run)
    t.daemon = True
    t.start()
    return s, t


def shutdown_server(s, t):
    s.close()
    if t.is_alive():
        t.join()


if __name__ == "__main__":

    from time import sleep

    s, t = start_server()

    while True:
        sleep(1)

    shutdown_server(s, t)
