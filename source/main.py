import sys
import logging

from globalvar import Globalvar
from exchangeThread import ExchangeThread
from bitpanda.enums import OrderSide

LOG = logging.getLogger("bitpanda")
LOG.setLevel(logging.DEBUG)
LOG.addHandler(logging.StreamHandler())


class Main:

    def __init__(self, image_paths, exchange_type=OrderSide.BUY.value):
        self.image_paths = image_paths.split(',')
        self.exchange_type = exchange_type
        self.glv = Globalvar()

    def start(self):
        threads = []
        for i, image_path in enumerate(self.image_paths):
            pixel_data = self.glv.get_image_pixel_data(image_path)

            image_data = self.glv.image_handler.extract_data(pixel_data)

            thread = ExchangeThread(self.glv, self.exchange_type, image_data)

            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()

        while len(threads) > 0:
            for i, t in enumerate(threads):
                if not t.is_running():
                    del(threads[i])


if __name__ == '__main__':
    # Given args must be the following
    # sys.args = [0 => 'python3', 1 => 'image_paths' joined by `,` , (2 => 'exchange_type')]

    if len(sys.argv) == 2:
        main = Main(sys.argv[1])
    elif len(sys.argv) == 3:
        main = Main(sys.argv[1], sys.argv[2].upper())
    else:
        image_paths = [
            "/home/erik/PycharmProjects/TrainingData/data/images_20/no/20-09-2022 01:09:32_DUSK.png",
            "/home/erik/PycharmProjects/TrainingData/data/images_20/no/20-09-2022 01:09:31_CRV.png",
            "/home/erik/Desktop/img/20-09-2022-06-42-56-XDB.png",
            "/home/erik/Desktop/img/20-09-2022-06-56-18-XDB.png",
            "/home/erik/PycharmProjects/TrainingData/data/images_20/no/20-09-2022 01:09:30_YFI.png"
        ]
        main = Main(','.join(image_paths))
    main.start()

    exit(0)
