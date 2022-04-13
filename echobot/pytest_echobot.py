

def test_echobot_start(bot, user):

    user.send_command('/start')

    message = user.get_message()

    assert message
    assert message['text'] == 'Hi [FN LN](tg://user?id=1)\!'


def test_echobot_help(bot, user):

    user.send_command('/help')

    message = user.get_message()

    assert message
    assert message['text'] == 'Help!'


def test_echobot_message(bot, user, user2):

    user.send_message('testing message')

    message = user.get_message()

    assert message
    assert message['text'] == 'testing message'

    user2.send_message('testing message')

    message = user2.get_message()

    assert message
    assert message['text'] == 'testing message'
