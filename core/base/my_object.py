import typing

import mongoengine as me

from .base_document import BaseDocument
from .base_model import BaseModel
from ..utils import cast

ObjectT = typing.TypeVar('ObjectT', bound='MyObject')


def get_model_name(obj: BaseModel | type[BaseModel]):
    if isinstance(obj, BaseModel):
        return obj.__class__.__name__
    return obj.__name__


class CurrentObject(BaseDocument):
    user_id: int = me.IntField()
    model: str = me.StringField()
    obj: dict = me.DictField()

    meta = {
        'collection': 'CurrentObjects',
    }


class CollectionObject(BaseDocument):
    user_id: int = me.IntField()
    model: str = me.StringField()
    obj: dict = me.DictField()

    meta = {
        'collection': 'CollectionObjects',
    }


class MyObject(BaseModel):
    """ Base class for all project objects """

    @classmethod
    def get(cls: type[ObjectT]) -> ObjectT | None:
        """ Get current object of current user from storage """
        from ..context import ctx

        doc = CurrentObject.get_doc(user_id=ctx.user_id, model=get_model_name(cls))

        if doc is None:
            return None
        else:
            return cast(doc.obj, cls)

    def save(self: ObjectT) -> ObjectT:
        """ Save object to storage as current for current user """
        from ..context import ctx

        doc = CurrentObject.get_doc(user_id=ctx.user_id, model=get_model_name(self))

        if doc is None:
            doc = CurrentObject(user_id=ctx.user_id, model=get_model_name(self))

        doc.obj = cast(self, dict)
        doc.save()

        return self
