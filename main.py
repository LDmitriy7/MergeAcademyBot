from dataclasses import dataclass

from core import *


@dataclass
class User(MyObject):
    ...


@on.command('start')
def welcome():
    if not User.get():
        req.send_message('<b>👋 Привiт Макс Соболь, дякую за реєстрацію</b>')
        User().save()

    req.send_message('<b>Обери що тебе цікавить 👇</b>')


run(
    parse_mode='html',
)
