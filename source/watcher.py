import time
import os

from globalvar import TRAINING_DATA_PATH
from globalvar import ACTION_IMAGES_PATH
from globalvar import LABEL_FOLDERS


class Watcher:

    def __init__(self, glv):
        self.glv = glv
        self.exchange_manager = self.glv.get_exchange_manager()
        self.thread_manager = self.glv.get_thread_manager()

    def watch(self):
        while True:
            self.watch_prediction_images()
            self.watch_action_images()

            time.sleep(1)

    def watch_action_images(self):
        action_images = os.listdir(ACTION_IMAGES_PATH)
        for file_name in action_images:
            self.exchange_manager.start(file_name)

    def watch_prediction_images(self):
        watch_path = TRAINING_DATA_PATH
        image_folders = os.listdir(watch_path)
        for image_folder in image_folders:
            label_folders = os.listdir(f'{watch_path}/{image_folder}')

            for label_folder in label_folders:
                if label_folder in LABEL_FOLDERS:
                    files = os.listdir(f'{watch_path}/{image_folder}/{label_folder}')
                    for file in files:
                        file_path = f'{watch_path}/{image_folder}/{label_folder}/{file}'
                        # prediction = self.predictor.predict(file_path)

                        # self.handle_prediction(prediction, file)
