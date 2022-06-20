import typing

import mongoengine as me

from .base import BaseDocument, BaseModel
from ..context import ctx

ModelT = typing.TypeVar('ModelT', bound='Model')


class CurrentObjects(BaseDocument):
    user_id: int = me.IntField()
    model: str = me.StringField()
    obj: dict = me.DictField()

    meta = {
        'collection': 'CurrentObjects__',
    }


class ObjectsCollections(BaseDocument):
    user_id: int = me.IntField()
    model: str = me.StringField()
    obj: dict = me.DictField()

    meta = {
        'collection': 'ObjectsCollections__',
    }


class MyObject(BaseModel):

    @classmethod
    def get(cls: type[ModelT]) -> ModelT | None:
        _doc = CurrentObjects.get_doc(user_id=ctx.user_id, model=cls.__name__)
        if _doc is None:
            return None
        else:
            _obj = cls.from_dict(_doc.obj)
        return _obj

    def save(self):
        _doc = CurrentObjects.get_doc(user_id=ctx.user_id, model=self.__class__.__name__)
        if _doc is None:
            _doc = CurrentObjects(user_id=ctx.user_id, model=self.__class__.__name__)
        _doc.obj = self.to_dict()
        _doc.save()
        return self
