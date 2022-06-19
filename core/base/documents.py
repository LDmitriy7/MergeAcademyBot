from __future__ import annotations

import mongoengine as me

from .base import BaseDocument

__all__ = [
    # 'CallbackButton',
    'Storage',
]


# class CallbackButton(BaseDocument):
#     _id: str = me.StringField(primary_key=True)
#     text: str = me.StringField()
#     button_id: str = me.StringField()
#     vars: dict = me.DictField()
#
#     meta = {
#         'collection': 'CallbackButtons__'
#     }


class UserKey(me.EmbeddedDocument):
    chat_id: int = me.IntField()
    user_id: int = me.IntField()


class Storage(BaseDocument):
    key: UserKey = me.EmbeddedDocumentField(UserKey, primary_key=True)
    state: str = me.StringField()
    lang: str = me.StringField()
    data: dict = me.DictField()
    models: dict[str, dict] = me.DictField()

    @classmethod
    def get(cls, chat_id: int, user_id: int) -> Storage:
        key = UserKey(chat_id=chat_id, user_id=user_id)
        return cls.get_doc(key=key) or Storage(key=key).save()

    meta = {
        'collection': 'Storage__'
    }
