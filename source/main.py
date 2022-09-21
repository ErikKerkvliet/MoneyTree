import sys
import logging
import time

from globalvar import Globalvar
from checkForFilesThread import CheckForFilesThread
from tickerThread import TickerThread
from threadManager import ThreadManager
from exchangeThread import ExchangeThread
from bitpanda.enums import OrderSide

LOG = logging.getLogger("bitpanda")
LOG.setLevel(logging.DEBUG)
LOG.addHandler(logging.StreamHandler())


class Main:

    def __init__(self, image_paths, exchange_type=None):
        self.image_paths = image_paths.split(',')
        self.exchange_type = exchange_type
        self.glv = Globalvar()
        self.threadManager = ThreadManager(self.glv)

    def start(self):
        self.threadManager.add(TickerThread(self.glv))

        for image_path in self.image_paths:
            self.image_found(image_path)

        self.threadManager.add(CheckForFilesThread(self.glv))

    def image_found(self, image_path):
        if '.png' not in image_path:
            self.problem_with_file(image_path)
            return

        pixel_data = self.glv.get_image_pixel_data(image_path)

        if not pixel_data:
            self.problem_with_file(image_path)
            return

        image_data = self.glv.image_handler.extract_data(pixel_data)

        exchange_type = self.exchange_type if self.exchange_type is not None else image_data['exchange_type']

        self.threadManager.add(ExchangeThread(self.glv, exchange_type, image_data))

    @staticmethod
    def problem_with_file(path):
        pass


if __name__ == '__main__':

    # Given args must be the following
    # sys.args = [0 => 'python3', 1 => 'image_paths' joined by `,` , (2 => 'exchange_type')]

    if len(sys.argv) == 2:
        main = Main(sys.argv[1])
    elif len(sys.argv) == 3:
        main = Main(sys.argv[1], sys.argv[2].upper())
    else:
        paths = [
            # "/home/erik/PycharmProjects/TrainingData/data/images_20/no/20-09-2022 01:09:32_DUSK.png",
            # "/home/erik/PycharmProjects/TrainingData/data/images_20/no/20-09-2022 01:09:31_CRV.png",
            # "/home/erik/PycharmProjects/TrainingData/data/images_20/no/20-09-2022 01:09:30_YFI.png"
        ]
        main = Main(','.join(paths), OrderSide.BUY.value)
    main.start()

    exit(0)
