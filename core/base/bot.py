import os
import typing

import requests

from ..base.base import TgMethod, TgObject

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

    resp = requests.post(endpoint, json=new_params)
    result = resp.json()['result']

    if issubclass(method.__response_type__, TgObject):
        return method.__response_type__.from_dict(result)
