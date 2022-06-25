from ...base import NewObject


class InlineKeyboard(NewObject):
    def add_row(self, *buttons):
        ...

    def add_rows(self, *buttons):
        ...

    def make(self):
        ...
