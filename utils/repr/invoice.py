from assets.my_models import Invoice
from assets import texts


def _repr_invoice(invoice: Invoice, lang: str) -> str:
    result = texts.invoice_ad_price.format(price=invoice.vacancies_price).get(lang)

    if invoice.pin_price:
        result += texts.invoice_pin_price.format(price=invoice.pin_price).get(lang) + '\n'

    if invoice.duplicate_price:
        result += texts.invoice_duplicate_price.format(price=invoice.duplicate_price).get(lang) + '\n'

    return result + texts.invoice_total_price.format(price=invoice.total_price).get(lang)


def repr_invoice(invoice: Invoice) -> texts.T:
    return texts.T(_repr_invoice(invoice, 'ru'), _repr_invoice(invoice, 'ua'))
