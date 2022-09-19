from imageHandler import ImageHandler
from bitpandaCalls import BitpandaCalls
from validate import Validate

from bitpanda.enums import OrderSide
from bitpanda.Pair import Pair

import time
import asyncio

DEFAULT_CURRENCY = 'EUR'


class ExchangeHandler:

    def __init__(self, glv, exchange_type=None):
        self.glv = glv
        self.validate = Validate()
        self.exchange_type = exchange_type
        self.bitpanda = BitpandaCalls(self.glv)
        self.image_handler = ImageHandler(self.glv)
        self.amount = 1

    def start(self, image_path):
        image_data = self.image_handler.extract_data(image_path)

        time.sleep(image_data['wait_time'])

        price = self.bitpanda.ticker(image_data['coin'], DEFAULT_CURRENCY)

        if not self.validate.by_price_and_old_price(price, image_data['price']):
            return

        exit()

        self.create_order(image_data)

    def create_order(self, exchange_data):
        exchange_type = self.exchange_type
        if self.exchange_type is None:
            exchange_type = self.get_action(exchange_data['exchange_type_id'])

        pair = self.get_pair(exchange_data['coin'], exchange_type)

        order_data = {
            'pair': pair,
            'exchange_type': exchange_type,
            'amount': self.amount,
        }

        loop = asyncio.get_event_loop()

        loop.run_until_complete(self.bitpanda.create_order(order_data))

        self.close(loop)

    def close(self, loop):
        loop.run_until_complete(self.bitpanda.close_client())

    @staticmethod
    def get_action(action):
        if action == 255:
            return OrderSide.BUY.value
        elif action == 127:
            return OrderSide.SELL.value
        elif action == 0:
            return False
        else:
            return None

    @staticmethod
    def get_pair(coin, exchange_type):
        if exchange_type == OrderSide.BUY.value:
            return Pair(coin, DEFAULT_CURRENCY)
        elif exchange_type == OrderSide.SELL.value:
            return Pair(DEFAULT_CURRENCY, coin)
        return None
