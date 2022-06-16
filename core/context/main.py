from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass

# from ..base.documents import Storage
# from ..base.new_objects import CallbackButton
from ..objects.tg_objects import Update, Message, CallbackQuery, Chat, User

UPDATE = ContextVar('UPDATE')


class ContextDict:

    def __init__(self, ctx: Context):
        self.ctx = ctx

    def __setitem__(self, key: str, value):
        storage = self.ctx.storage
        storage.data[key] = value
        storage.save()

    def __getitem__(self, item: str):
        storage = self.ctx.storage
        return storage.data[item]

    def __contains__(self, key: str):
        storage = self.ctx.storage
        return key in storage.data

    def get(self, item: str, default=None):
        try:
            return self[item]
        except KeyError:
            return default

    def clear(self):
        storage = self.ctx.storage
        storage.data.clear()
        storage.save()


@dataclass
class Context:
    token: str = None
    parse_mode: str = None
    disable_web_page_preview: bool = None
    disable_notification: bool = None
    protect_content: bool = None

    @property
    def data(self):
        return ContextDict(self)

    @property
    def storage(self):
        return Storage.get(ctx.chat_id, ctx.user_id)

    @property
    def state(self) -> str | None:
        """User.state"""
        return self.storage.state

    @state.setter
    def state(self, value: str):
        """User.state"""
        storage = self.storage
        storage.state = value
        storage.save()

    @property
    def lang(self) -> str | None:
        """User.lang"""
        return self.storage.lang

    @lang.setter
    def lang(self, value: str):
        """User.lang"""
        storage = self.storage
        storage.lang = value
        storage.save()

    @property
    def button(self) -> CallbackButton | None:
        """CallbackQuery.button"""
        try:
            button_id = self.query_data
            return CallbackButton.get_button(button_id)
        except (KeyError, AttributeError):
            return None

    @property
    def update(self) -> Update | None:
        """ Update """
        return UPDATE.get(None)

    @update.setter
    def update(self, value: Update):
        UPDATE.set(value)

    @property
    def callback_query(self) -> CallbackQuery | None:
        """ CallbackQuery """
        value = None

        if update := self.update:
            value = update.callback_query

        return value

    @property
    def callback_query_id(self) -> str | None:
        """ CallbackQuery.id """
        value = None

        if callback_query := self.callback_query:
            value = callback_query.id

        return value

    @property
    def message(self) -> Message | None:
        """ Message | ChannelPost | CallbackQuery.message """
        value = None

        if update := self.update:
            value = update.message or update.channel_post

            if value is None:
                if callback_query := self.callback_query:
                    value = callback_query.message

        return value

    @property
    def message_id(self) -> int | None:
        """ Message.id | ChannelPost.id | CallbackQuery.message.id """
        value = None

        if message := self.message:
            value = message.message_id

        return value

    @property
    def chat(self) -> Chat | None:
        """ Message.chat | ChannelPost.chat | CallbackQuery.chat """

        value = None

        if message := self.message:
            value = message.chat

        return value

    @property
    def chat_id(self) -> int | None:
        """ Message.chat.id | ChannelPost.chat.id | CallbackQuery.chat.id """
        value = None

        if chat := self.chat:
            value = chat.id

        return value

    @property
    def chat_type(self) -> int | None:
        """ Message.chat.type | ChannelPost.chat.type | CallbackQuery.chat.type """
        value = None

        if chat := self.chat:
            value = chat.type

        return value

    @property
    def text(self) -> str | None:
        """ Message.text | ChannelPost.text | CallbackQuery.message.text """
        value = None

        if message := self.message:
            value = message.text

        return value

    @property
    def query_data(self) -> str | None:
        """ CallbackQuery.data """

        value = None

        if callback_query := self.callback_query:
            value = callback_query.data

        return value

    @property
    def user(self) -> User | None:
        """ Message.user | CallbackQuery.user """
        value = None

        if update := self.update:
            if message := update.message:
                value = message.from_user
            elif callback_query := update.callback_query:
                value = callback_query.from_user

        return value

    @property
    def user_id(self) -> int | None:
        """ Message.user.id | CallbackQuery.user.id """
        value = None

        if user := self.user:
            value = user.id

        return value
