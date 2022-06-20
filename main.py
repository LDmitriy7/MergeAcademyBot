from assets.my_objects import User
from core import *


@on.command('start')
def welcome():
    if not User.get():
        req.send_message(f'<b>👋 Привiт {ctx.user.first_name}, дякую за реєстрацію</b>')
        User().save()

    req.send_message('<b>Обери що тебе цікавить 👇</b>')


run(
    parse_mode='html',
)
