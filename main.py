from assets import *
from core import *


@on.command('start')
def welcome():
    if not my_obj.User.get():
        req.send_message(f'<b>👋 Привiт {ctx.user.first_name}, дякую за реєстрацію</b>')
        my_obj.User().save()

    req.send_message('<b>Обери що тебе цікавить 👇</b>')


run(
    parse_mode='html',
)
