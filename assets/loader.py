from utils import Merchant
from . import config

merchant = Merchant(
    config.MERCHANT_ID,
    config.MERCHANT_SECRET_KEY,
    f'{config.HOST}{config.PAYMENT_ENDPOINT}'
)
