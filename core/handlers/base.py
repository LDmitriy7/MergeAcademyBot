import typing
from dataclasses import dataclass, field

from ..filters.base import Filter


@dataclass
class Handler:
    func: typing.Callable[[], None]
    filters: list[Filter] = field(default_factory=list)
    exclusive: bool = True

    _check_first = False
    _check_last = False
    _check_after_any = False

    @property
    def check_first(self):
        return self._check_first

    @check_first.setter
    def check_first(self, value: bool):
        self._check_first = value

    @property
    def check_last(self):
        return self._check_last

    @check_last.setter
    def check_last(self, value: bool):
        self._check_last = value

    @property
    def check_after_any(self):
        return self._check_after_any

    @check_after_any.setter
    def check_after_any(self, value: bool):
        self._check_after_any = value
