from .context_dict import ContextDict
from .layer1 import ContextLayer1
from .storage import Storage

from ..objects import CallbackButton


class ContextLayer2(ContextLayer1):

    @property
    def _storage(self):
        return Storage.get(self.user.id)

    @property
    def data(self):
        return ContextDict(self._storage)

    @property
    def state(self) -> str | None:
        """ User.state """
        return self._storage.state

    @state.setter
    def state(self, value: str):
        storage = self._storage
        storage.state = value
        storage.save()

    @property
    def lang(self) -> str | None:
        """ User.lang """
        return self._storage.lang

    @lang.setter
    def lang(self, value: str):
        storage = self._storage
        storage.lang = value
        storage.save()

    # @property
    # def button(self) -> CallbackButton | None:
    #     """ CallbackQuery.button """
    #     try:
    #         button_id = self.callback_query.data
    #         return CallbackButton.get_button(button_id)
    #     except (KeyError, AttributeError):
    #         return None
