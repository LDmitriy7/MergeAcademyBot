from .base import Handler

handlers: list[Handler] = []
pre_handlers: list[Handler] = []
post_handlers: list[Handler] = []
post_any_handlers: list[Handler] = []
