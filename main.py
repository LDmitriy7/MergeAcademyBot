from assets import *
from core import *


@on.command('start')
def welcome():
    if not my_objects.User.get():
        request.send_message(f'<b>👋 Привiт {ctx.user.first_name}, дякую за реєстрацію</b>')
        my_objects.User().save()

    request.send_message('<b>Обери що тебе цікавить 👇</b>')


@on.text(kb.Main.master_class)
def master_class():
    request.send_message('ℹ️ Зараз немає доступних майстер-класів')


run(
    parse_mode='html',
)
