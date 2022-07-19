from assets import *
from core import *


@on.button(kb.MainMenu.my_ads)
def my_ads():
    bot.answer_callback_query(texts.no_my_ads)
