from validate import Validate
from testing import Testing
from bitpanda.enums import OrderSide
from bitpanda.Pair import Pair

import time
import asyncio
import globalvar


class ExchangeHandler:

    def __init__(self, parent=None, glv=None, exchange_type=None):
        self.parent = parent
        self.glv = glv if parent is None else parent.glv
        self.exchange_type = exchange_type if exchange_type is not None else parent.exchange_type
        self.amount = 1

        self.validate = Validate(self.glv)
        self.testing = Testing(self.glv)
        self.bitpanda = self.glv.get_bitpanda_calls()

    def start(self, extracted: dict) -> bool:

        if globalvar.TESTING:
            self.testing.test(extracted)
            return False

        # self.create_order(extracted)

        time.sleep(extracted['wait_time'])

        if not self.validate.by_price_coin(extracted['price'], extracted['coin']):
            self.stop_thread()
            return False

        self.exchange_type = OrderSide.BUY.value if self.exchange_type == OrderSide.SELL.value else OrderSide.SELL.value

        if globalvar.TESTING:
            self.testing.test(extracted)
            self.stop_thread()
            return False

        # self.create_order(extracted)
        print(self.exchange_type)
        self.stop_thread()

        return True

    def create_order(self, exchange_data):
        pair = self.get_pair(exchange_data['coin'], self.exchange_type)

        order_data = {
            'pair': pair,
            'exchange_type': self.exchange_type,
            'amount': self.amount,
        }

        loop = asyncio.get_event_loop()

        loop.run_until_complete(self.bitpanda.create_order(order_data))

        self.close_loop(loop)

    def stop_thread(self):
        if self.parent is not None:
            self.parent.stop()

    def close_loop(self, loop):
        loop.run_until_complete(self.bitpanda.close_client())

    def get_pair(self, coin, exchange_type):
        if exchange_type == OrderSide.BUY.value:
            return Pair(coin, globalvar.DEFAULT_CURRENCY)
        elif exchange_type == OrderSide.SELL.value:
            return Pair(globalvar.DEFAULT_CURRENCY, coin)
        return None
