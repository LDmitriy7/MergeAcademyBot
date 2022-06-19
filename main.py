import typing
from dataclasses import dataclass
import mongoengine as me
from core import *

T = typing.TypeVar('T')

me.connect('MergeAcademyBot')


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

    req.send_message('<b>Обери що тебе цікавить 👇</b>')


run(
    parse_mode='html',
)
# fix parse_mode=None unsupported
