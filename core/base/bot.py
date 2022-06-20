import logging
import os
import typing

import mongoengine as me
import requests

from ..base.base import TgMethod, TgObject, prepare_value
from ..utils import listify

logger = logging.getLogger('bot')
BOT_TOKEN = os.environ['BOT_TOKEN']
DB_NAME = os.environ['DB_NAME']
API_URL = 'https://api.telegram.org/bot{}/{}'

me.connect(DB_NAME)


def clear_params(params: dict) -> dict:
    return {key: value for key, value in params.items() if value is not None}


def request(method: type[TgMethod], params: dict, **alternatives) -> TgObject | typing.Any:
    endpoint = API_URL.format(BOT_TOKEN, method.__name__)

    new_params = params.copy()

    for key, value in alternatives.items():
        new_params[key] = alternatives[key] if params[key] is None else params[key]

    new_params = clear_params(new_params)

    resp = requests.post(endpoint, json=new_params).json()
    if resp['ok']:
        result = resp['result']
    else:
        raise Exception(f'{resp["error_code"]=}, {resp["description"]=}')

    cast_types = listify(getattr(method.__response_type__, '__args__', method.__response_type__))
    result = prepare_value(result, cast_types)
    return result
