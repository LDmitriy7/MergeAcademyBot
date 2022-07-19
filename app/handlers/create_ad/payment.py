from bson import ObjectId

from assets import *
from core import *
from utils import repr_invoice

conv = states.CreateAd


def get_self_url():
    me = bot.get_me()
    return f'https://t.me/{me.username}'


@on.button(kb.EditAd.finish, state=conv.ad_preview)
def _():
    ad = my_models.Ad.get()
    vacancies_amount = len(ad.vacancies)
    invoice = my_models.Invoice(
        vacancies_price=config.AD_PRICE_BY_VACANCIES_AMOUNT[vacancies_amount]
    )

    if ad.pin_option:
        invoice.pin_price = config.PIN_PRICE

    if ad.duplicate_option:
        invoice.duplicate_price = config.DUPLICATE_PRICE_BY_VACANCIES_AMOUNT[vacancies_amount]

    with my_models.Order.proxy() as order:
        order.id = str(ObjectId())
        order.ad = ad
        order.price = invoice.total_price

    payment_url = merchant.get_invoice_url(order.id, invoice.total_price, get_self_url())
    bot.send_message(repr_invoice(invoice), reply_markup=kb.Payment(payment_url))
