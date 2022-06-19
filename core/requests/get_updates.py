from ..base import bot
from ..methods import GetUpdates
from ..objects.tg_objects import Update


def get_updates(
        offset: int = None,
        limit: int = None,
        timeout: int = None,
        allowed_updates: list[str] = None,
) -> list[Update]:
    updates = bot.request(
        GetUpdates,
        locals(),
    )
    return [Update.from_dict(u) for u in updates]  # TODO
