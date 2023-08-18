

def test_bot_start(bot, user):

    user.send_command('/start')

    message = user.get_message()

    assert message
    assert message['text'] == 'Hi [FirstName LastName](tg://user?id=1)\!'


def test_bot_help(bot, user):

    user.send_command('/help')

    message = user.get_message()

    assert message
    assert message['text'] == 'Help!'


def test_bot_message(bot, user):

    user.send_message('testing message')

    message = user.get_message()

    assert message
    assert message['text'] == 'testing message'


def test_bot_multiple_users(bot, user, user2):

    user.send_message('my name user1')

    message = user.get_message()

    assert message
    assert message['text'] == 'my name user1'

    user2.send_message('my name user2')

    message = user2.get_message()

    assert message
    assert message['text'] == 'my name user2'


def test_bot_edit_message(bot, user):

    user.send_command('/edit')

    messages = user.get_messages(2)

    assert len(messages) == 2
    assert messages[0]['text'] == 'first message'
    assert messages[1]['text'] == 'second message'
