from ..base import bot
from ..methods import GetUpdates
from ..objects.tg_objects import Update


def get_updates(
        offset: int = None,
        limit: int = None,
        timeout: int = None,
        allowed_updates: list[str] = None,
) -> list[Update]:
    return bot.request(
        GetUpdates,
        locals(),
    )
