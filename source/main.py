import asyncio
import sys
import logging
import time

from handleImage import HandleImage
from globalvar import Globalvar
from handleExchange import HandleExchange
from bitpanda.enums import OrderSide

# from bitpanda.subscriptions import AccountSubscription, PricesSubscription, OrderbookSubscription, \
#     CandlesticksSubscription, MarketTickerSubscription, CandlesticksSubscriptionParams
LOG = logging.getLogger("bitpanda")
LOG.setLevel(logging.DEBUG)
LOG.addHandler(logging.StreamHandler())


class Main:

    def __init__(self, image_paths, exchange_type=OrderSide.BUY.value):
        self.image_paths = image_paths
        self.glv = Globalvar()
        self.handle_image = HandleImage(self.glv)
        self.handle_exchange = HandleExchange(self.glv, exchange_type)

    def start(self):
        loop = asyncio.get_event_loop()
        for image_path in self.image_paths.split(','):
            self.handle_image.extract_data(image_path)

            info = self.handle_exchange.ticker(self.glv.coin, 'EUR')
            print(self.glv.coin, self.glv.price)
            # for coin in self.glv.coins:
            exit()
            loop.run_until_complete(self.handle_exchange.get_currencies(self.glv.coin))

            # loop.run_until_complete(self.handle_exchange.create_order())
            time.sleep(self.glv.get_result_time())

            # self.handle_exchange.ticker(self.glv.coin)['EUR']

        self.exit(loop)

    def exit(self, loop=None):
        if loop is not None:
            loop.run_until_complete(self.handle_exchange.close_client())
        exit()


if __name__ == '__main__':
    # Given args must be the following
    # sys.args = [0 => 'python3', 1 => 'image_paths' joined by `,` , (2 => 'exchange_type')]

    if len(sys.argv) == 2:
        main = Main(sys.argv[1])
    elif len(sys.argv) == 3:
        main = Main(sys.argv[1], sys.argv[2].upper())
    else:
        main = Main("/home/erik/PycharmProjects/TrainingData/source/data/images_20/no/18-09-2022 15:36:45_BTC.png")

    main.start()
    exit()
