from assets import *
from core import *


@on.button(kb.MainMenu.change_lang)
def change_lang():
    if ctx.lang == 'ua':
        ctx.lang = 'ru'
    else:
        ctx.lang = 'ua'

    bot.edit_message_text(texts.main_menu, reply_markup=kb.MainMenu(ctx.lang))
