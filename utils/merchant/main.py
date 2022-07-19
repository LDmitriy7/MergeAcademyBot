from cloudipsp import Api, Checkout
from cloudipsp.configuration import __protocol__
from cloudipsp.helpers import is_approved


class Merchant:

    def __init__(self, merchant_id: str, secret_key: str, server_callback_url: str):
        self.api = Api(merchant_id=merchant_id, secret_key=secret_key)
        self.checkout = Checkout(api=self.api)
        self.server_callback_url = server_callback_url

    def get_invoice_url(self, order_id: str, price: int, bot_url: str):
        resp = self.checkout.url({
            'currency': 'UAH',
            'order_desc': 'Оплата за размещение',
            'amount': price * 100,
            'order_id': order_id,
            'server_callback_url': self.server_callback_url,
            'response_url': bot_url,
        })
        return resp['checkout_url']

    def check_payment(self, data: dict):
        try:
            result = is_approved(data, self.api.secret_key, __protocol__)
        except:  # TODO
            result = False

        return result
