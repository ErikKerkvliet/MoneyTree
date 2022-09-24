import sys
import logging

from globalvar import Globalvar
from make import Make
from tickerThread import TickerThread
from watcher import Watcher
from bitpanda.enums import OrderSide

LOG = logging.getLogger("bitpanda")
LOG.setLevel(logging.DEBUG)
LOG.addHandler(logging.StreamHandler())


class Main:

    def __init__(self, image_paths, exchange_type=None):
        self.image_paths = image_paths.split(',')
        self.exchange_type = exchange_type

        self.glv = Globalvar()
        self.make = Make()

        self.watcher = Watcher(self.glv)
        self.thread_manager = self.glv.get_thread_manager()

    def start(self):
        self.thread_manager.add(TickerThread(self.glv))

        self.watcher.watch()


if __name__ == '__main__':

    # Given args must be the following
    # sys.args = [0 => 'python3', 1 => 'image_paths' joined by `,` , (2 => 'exchange_type')]

    if len(sys.argv) == 2:
        main = Main(sys.argv[1])
    elif len(sys.argv) == 3:
        main = Main(sys.argv[1], sys.argv[2].upper())
    else:
        paths = [
            "/home/erik/PycharmProjects/TrainingData/data/images_50/no/23-09-2022 01:04:25_DOT.png",
            "/home/erik/PycharmProjects/TrainingData/data/images_50/no/23-09-2022 01:04:27_ENJ.png",
            "/home/erik/PycharmProjects/TrainingData/data/images_50/no/23-09-2022 01:04:28_LSK.png"
        ]
        main = Main(','.join(paths), OrderSide.BUY.value)
    main.start()

    exit(0)
