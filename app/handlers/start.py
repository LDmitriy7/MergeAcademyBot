from assets import *
from core import *


@on.command('start', state='*')
def start():
    ctx.state = None

    if not ctx.lang:
        ctx.lang = 'ru'

    ctx.delete_current_models()
    bot.send_message(texts.main_menu, reply_markup=kb.MainMenu(ctx.lang))


start.check_first = True
