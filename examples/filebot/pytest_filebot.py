import os
import io


def test_echobot_start(bot, user):

    user.send_command('/start')

    message = user.get_message()

    assert message
    assert message['text'] == 'Hi!'


def test_echobot_file(bot, user):

    current_dir = os.path.dirname(os.path.abspath(__file__))

    user.send_document(current_dir, 'test.txt')

    document = user.get_document()

    file_io = document.path_or_bytes
    assert file_io.name == 'echo_test.txt'

    content = io.TextIOWrapper(file_io, encoding='utf-8').read()
    assert content == 'Hello world!\nHello world!'
