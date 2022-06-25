from .layer2 import ContextLayer2


class ContextLayer3(ContextLayer2):

    @property
    def user_id(self) -> int | None:
        """ Message.user.id | CallbackQuery.user.id """
        value = None

        if user := self.user:
            value = user.id

        return value

    @property
    def query_data(self) -> str | None:
        """ CallbackQuery.data """

        value = None

        if callback_query := self.callback_query:
            value = callback_query.data

        return value

    @property
    def text(self) -> str | None:
        """ Message.text | ChannelPost.text | CallbackQuery.message.text """
        value = None

        if message := self.message:
            value = message.text

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
    def callback_query_id(self) -> str | None:
        """ CallbackQuery.id """
        value = None

        if callback_query := self.callback_query:
            value = callback_query.id

        return value

    @property
    def message_id(self) -> int | None:
        """ Message.id | ChannelPost.id | CallbackQuery.message.id """
        value = None

        if message := self.message:
            value = message.message_id

        return value
