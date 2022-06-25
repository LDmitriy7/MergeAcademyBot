from __future__ import annotations

import mongoengine as me

from ...base import BaseDocument, NewObject


class CallbackButtonDoc(BaseDocument):
    id: str = me.StringField()
    vars: dict = me.DictField()

    meta = {
        'collection': 'CallbackButtons'
    }


class CallbackButton(NewObject):
    """ CallbackButton """
