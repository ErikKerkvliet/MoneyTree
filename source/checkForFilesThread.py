import threading
import os
import time

from globalvar import ACTION_IMAGES_PATH
from threadManager import ThreadManager
from exchangeThread import ExchangeThread


class CheckForFilesThread(threading.Thread):
    def __init__(self, glv):
        threading.Thread.__init__(self, name='check_for_files')
        self._running = True
        self.glv = glv
        self.threadManager = ThreadManager(self.glv)
        self.exchange_type = None

    def run(self):
        while True:
            action_images = os.listdir(ACTION_IMAGES_PATH)
            for image_path in action_images:
                self.start_exchange(f'{ACTION_IMAGES_PATH}/{image_path}')

            time.sleep(1)

        self.stop()
        return

    def stop(self) -> None:
        self._running = False

    def is_running(self) -> bool:
        return self._running

    def start_exchange(self, image_path):
        if '.png' not in image_path:
            return

        pixel_data = self.glv.get_image_pixel_data(image_path)

        if not pixel_data:
            return

        image_data = self.glv.image_handler.extract_data(pixel_data)

        exchange_type = self.exchange_type if self.exchange_type is not None else image_data['exchange_type']

        self.threadManager.add(ExchangeThread(self.glv, exchange_type, image_data))
