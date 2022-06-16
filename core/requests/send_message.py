from .base import ReplyMarkupT
from ..base import bot
from ..base.new_objects import Translations
from ..context import ctx
from ..methods import SendMessage
from ..objects.tg_objects import MessageEntity, Message


class Context:
    chat_id = 724477101
    parse_mode = 'html'
    disable_web_page_preview = True
    disable_notification = True
    protect_content = False


ctx = Context()


def send_message(
        text: str | Translations,
        reply_markup: ReplyMarkupT = None,

        chat_id: int | str = None,
        parse_mode: str = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,

        reply_to_message_id: int = None,
        entities: list[MessageEntity] = None,
        allow_sending_without_reply: bool = None,
) -> Message:
    return bot.request(
        SendMessage,
        locals(),
        chat_id=ctx.chat_id,
        parse_mode=ctx.parse_mode,
        disable_web_page_preview=ctx.disable_web_page_preview,
        disable_notification=ctx.disable_notification,
        protect_content=ctx.protect_content,
    )
