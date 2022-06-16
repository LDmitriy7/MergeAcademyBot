import typing
from dataclasses import dataclass

from core import *
from core.handlers.loader import handlers

T = typing.TypeVar('T')


class Model:

    @classmethod
    def get(cls: type[T]) -> T | None:
        return None


@dataclass
class User(Model):
    id: int


@on.command('start')
def welcome():
    if not User.get():
        req.send_message('<b>👋 Привiт Макс Соболь, дякую за реєстрацію</b>')

    msg = req.send_message('<b>Обери що тебе цікавить 👇</b>')
    print(isinstance(msg, obj.Message))


welcome.exclusive = False

print(handlers)
