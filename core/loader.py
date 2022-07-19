import logging

import mongoengine
import requests
from envparse import env

from .handlers.base import Handler

env.read_envfile()

BOT_TOKEN = env('BOT_TOKEN')
DB_NAME = env('DB_NAME')

logger = logging.getLogger('bot')
mongoengine.connect(DB_NAME)
session = requests.Session()

HANDLERS: list[Handler] = []
