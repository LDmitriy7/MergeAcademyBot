import logging

from assets import *
from core import *

logging.basicConfig(level=20)


@on.command('start')
def welcome():
    if not my_objects.User.get():
        bot.send_message(f'<b>👋 Привiт {ctx.user.first_name}, дякую за реєстрацію</b>')
        my_objects.User().save()

    bot.send_message('<b>Обери що тебе цікавить 👇</b>')


@on.command('test')
def test():
    bot.send_message('')


@on.text(kb.Main.master_class)
def master_class():
    bot.send_message('ℹ️ Зараз немає доступних майстер-класів')


run(
    parse_mode='html',
)
