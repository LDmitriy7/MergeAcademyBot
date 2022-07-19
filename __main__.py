import logging

import app
from core import run

app.init()

logging.basicConfig(level=30)

run(
    skip_updates=True,
    parse_mode='html',
)
