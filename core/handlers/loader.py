from .base import Handler

HANDLERS: list[Handler] = []
PRE_HANDLERS: list[Handler] = []
POST_HANDLERS: list[Handler] = []
POST_ANY_HANDLERS: list[Handler] = []
