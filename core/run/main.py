from ..context import ctx
from ..loader import HANDLERS, logger
from ..objects.tg_objects import Update
from ..requests.get_updates import get_updates


def notify_handlers():
    for handler in HANDLERS:
        for _filter in handler.filters:
            if not _filter():
                break
        else:
            handler.func()
            break


def process_update(update: Update) -> None:
    ctx.update = update
    notify_handlers()
    ctx.update = None


def process_updates(updates: list[Update]):
    for update in updates:
        process_update(update)


def start_polling():
    offset = None

    while True:
        try:
            updates = get_updates(offset=offset)

            if updates:
                logger.info(updates)
                offset = updates[-1].update_id + 1
                process_updates(updates)
        except Exception as exc:
            logger.exception(exc)


def run(
        parse_mode: str = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
):
    logger.info('Starting up...')

    ctx.parse_mode = parse_mode
    ctx.disable_web_page_preview = disable_web_page_preview
    ctx.disable_notification = disable_notification
    ctx.protect_content = protect_content

    try:
        start_polling()
    except KeyboardInterrupt:
        logger.info('Shutting down...')
