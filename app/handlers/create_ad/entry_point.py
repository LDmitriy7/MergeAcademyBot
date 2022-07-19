from assets import *
from core import *

EDIT_MODE = 'edit_mode'


@on.button(kb.MainMenu.create_ad)
def create_ad():
    ctx.data[EDIT_MODE] = False
    ctx.state = states.CreateAd.region
    bot.send_message(texts.create_ad_info)
    bot.send_message(texts.ask_region, reply_markup=kb.Regions())


