from exchangeThread import ExchangeThread

from globalvar import ACTION_IMAGES_PATH


class ExchangeManager:

    def __init__(self, glv, exchange_type=None):
        self.glv = glv
        self.exchange_type = exchange_type
        self.thread_manager = self.glv.get_thread_manager()
        self.image_handler = self.glv.get_image_handler()

    def start(self, file_name):
        if '.png' not in file_name:
            return

        pixel_data = self.image_handler.get_image_pixel_data(f'{ACTION_IMAGES_PATH}/{file_name}')

        if not pixel_data:
            return

        image_data = self.image_handler.extract_data(pixel_data)
        image_data['name'] = file_name

        exchange_type = self.exchange_type if self.exchange_type is not None else image_data['exchange_type']

        self.thread_manager.add(ExchangeThread(self.glv, exchange_type, image_data))
