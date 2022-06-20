from .base import NewObject


class Translations(NewObject):
    ...


class Keyboard(NewObject):
    def add_rows(self, *buttons):
        ...

    def make(self):
        ...
