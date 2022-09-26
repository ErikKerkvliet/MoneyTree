import threading
import os
import time

from threadManager import ThreadManager
from exchangeThread import ExchangeThread


class WatcherThread(threading.Thread):
    def __init__(self, glv):
        threading.Thread.__init__(self, name='watcher_thread')
        self.glv = glv
        self.thread_manager = ThreadManager(self.glv)
        self.predictor = self.glv.get_predictor()
        self.exchange_type = None

    def run(self):
        while True:
            self.watch(self.glv.TRAINING_DATA_PATH)
            action_images = os.listdir(self.glv.ACTION_IMAGES_PATH)
            for file_name in action_images:
                self.start_exchange(file_name)

            time.sleep(1)

        self.stop()
        return

    def stop(self) -> None:
        self._running = False

    def is_running(self) -> bool:
        return self._running

    def watch(self, watch_path):
        image_folders = os.listdir(watch_path)
        for image_folder in image_folders:
            label_folders = os.listdir(f'{watch_path}/{image_folder}')

            for label_folder in label_folders:
                if label_folder in self.glv.LABEL_FOLDERS:
                    files = os.listdir(f'{watch_path}/{image_folder}/{label_folder}')
                    for file in files:
                        file_path = f'{watch_path}/{image_folder}/{label_folder}/{file}'
                        # prediction = self.predictor.predict(file_path)
                        #
                        # self.handle_prediction(prediction, file)

        time.sleep(1)

    def handle_prediction(self, prediction, file_path):
        # for key in self.glv.PREDICTIONS.keys():
        if prediction == self.glv.PREDICTIONS.keys()[0]:
            self.start_exchange(file_path)
            self.glv.move_file(file_path)

    def start_exchange(self, file_name):
        if '.png' not in file_name:
            return

        pixel_data = self.glv.get_image_handler().get_image_pixel_data(f'{self.glv.ACTION_IMAGES_PATH}/{file_name}')

        if not pixel_data:
            return

        image_data = self.glv.image_handler.extract_data(pixel_data)
        image_data['name'] = file_name

        exchange_type = self.exchange_type if self.exchange_type is not None else image_data['exchange_type']

        self.thread_manager.add(ExchangeThread(self.glv, exchange_type, image_data))
