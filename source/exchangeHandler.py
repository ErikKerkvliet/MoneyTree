from validate import Validate

from bitpanda.enums import OrderSide
from bitpanda.Pair import Pair

import time
import asyncio

DEFAULT_CURRENCY = 'EUR'


class ExchangeHandler:

    def __init__(self, parent=None, glv=None, exchange_type=None):
        self.parent = parent
        self.glv = glv if parent is None else parent.glv
        self.exchange_type = exchange_type if parent is None else parent.exchange_type
        self.amount = 1

        self.validate = Validate()
        self.bitpanda = self.glv.get_bitpanda_calls()

    def start(self, extracted_data: dict):
        # time.sleep(extracted_data['wait_time'])

        price = self.bitpanda.ticker(extracted_data['coin'], DEFAULT_CURRENCY)

        print(f'Coin: {extracted_data["coin"]},', f'Image: {extracted_data["price"]},', f'Current: {price}')
        if not self.validate.by_price_and_old_price(price, extracted_data['price']):
            return False

        # self.create_order(extracted_data)

        if self.parent is not None:
            self.parent.stop()

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
