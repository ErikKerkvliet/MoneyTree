import sys
import logging
import _thread

from globalvar import Globalvar
from exchangeHandler import ExchangeHandler
from bitpanda.enums import OrderSide

# from bitpanda.subscriptions import AccountSubscription, PricesSubscription, OrderbookSubscription, \
#     CandlesticksSubscription, MarketTickerSubscription, CandlesticksSubscriptionParams
LOG = logging.getLogger("bitpanda")
LOG.setLevel(logging.DEBUG)
LOG.addHandler(logging.StreamHandler())


class Main:

    def __init__(self, image_paths, exchange_type=OrderSide.BUY.value):
        self.image_paths = image_paths.split(',')
        self.exchange_type = exchange_type
        self.glv = Globalvar()

    def start(self):
        for image_path in self.image_paths:
            try:
                _thread.start_new_thread(self.start_exchange, (image_path,))
            except:
                print("Error: unable to start thread")

    def start_exchange(self, image_path):
        ExchangeHandler(self.glv, self.exchange_type).start(image_path)


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
