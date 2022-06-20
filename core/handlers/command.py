from .base import Handler
from .loader import HANDLERS
from .. import filters


def command(
        value: str = None,
        user_id: int | list[int] = None,
        chat_type: str | list[str] = None,
        state: str = None,
):
    _filters = [
        filters.Command(value),
        filters.State(state),
    ]

    if user_id:
        _filters.append(filters.UserId(user_id))

    if chat_type:
        _filters.append(filters.ChatType(chat_type))

    def _(func):
        handler = Handler(func, _filters)
        HANDLERS.append(handler)
        return handler

    return _
