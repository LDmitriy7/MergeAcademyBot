import os
import time
import typing
from ..context import ctx
from ..handlers.loader import handlers
import requests
import logging
from ..base.base import TgMethod, TgObject
from ..objects.tg_objects import Update
from ..requests.get_updates import get_updates

logger = logging.getLogger('bot')
BOT_TOKEN = os.environ['BOT_TOKEN']
API_URL = 'https://api.telegram.org/bot{}/{}'


def clear_params(params: dict) -> dict:
    return {key: value for key, value in params.items() if value is not None}


def request(method: type[TgMethod], params: dict, **alternatives) -> TgObject | typing.Any:
    from .base import TgObject

    endpoint = API_URL.format(BOT_TOKEN, method.__name__)

    new_params = clear_params(params)

    for key, value in alternatives.items():
        new_params[key] = alternatives[key] if params[key] is None else params[key]

    resp = requests.post(endpoint, json=new_params).json()
    if resp['ok']:
        result = resp['result']
    else:
        raise Exception(f'{resp["error_code"]=}, {resp["description"]=}')

    if issubclass(method.__response_type__, TgObject):
        return method.__response_type__.from_dict(result)
    return result


# ===

def _check_handlers(update: Update):
    for handler in handlers:
        for _filter in handler.filters:
            if not _filter():
                break
        else:
            handler.func()


def process_update(update: Update) -> None:
    ctx.update = update

    try:
        _check_handlers(update)
    # except exceptions.Cancel:
    #     pass
    except Exception as exc:
        logger.exception(exc)

    # ctx.update = None #TODO


def _process_updates(updates: list[Update]):
    for update in updates:
        process_update(update)


def _start_polling(poll_interval: float):
    offset = None

    while True:
        try:
            updates = get_updates(offset=offset)

            if updates:
                logger.info(updates)
                _process_updates(updates)
                offset = updates[-1].update_id + 1

            time.sleep(poll_interval)
        except Exception as exc:
            logger.exception(exc)


# def _import_all(package: str):
#     dirname = package.replace('.', '/')
#     for file in Path(dirname).glob('*.py'):
#         if not file.stem.startswith('_'):
#             import_module(f'.{file.stem}', package)
#
#
# APP_MODULES = ['handlers', 'middlewares', 'tasks']
#
#
# def _init_app():
#     import app
#
#     if hasattr(app, 'init'):
#         app.init()
#     else:
#         for m_name in APP_MODULES:
#             module = import_module(f'app.{m_name}')
#             if hasattr(module, 'setup'):
#                 module.setup()
#             else:
#                 _import_all(f'app.{m_name}')
#
#
def run(
        parse_mode: str = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        poll_interval: float = 0.0,
):
    #     _init_app()

    logger.info('Starting up...')

    ctx.parse_mode = parse_mode
    ctx.disable_web_page_preview = disable_web_page_preview
    ctx.disable_notification = disable_notification
    ctx.protect_content = protect_content

    try:
        _start_polling(poll_interval)
    except KeyboardInterrupt:
        logger.info('Shutting down...')
