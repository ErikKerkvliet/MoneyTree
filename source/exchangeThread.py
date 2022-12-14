import threading

from exchangeHandler import ExchangeHandler


class ExchangeThread(threading.Thread):
    def __init__(self, glv, exchange_type, image_data):
        threading.Thread.__init__(self, name='exchange')
        self._running = True
        self.glv = glv
        self.exchange_type = exchange_type
        self.image_data = image_data

    def run(self):
        if ExchangeHandler(self, self.glv, self.exchange_type).start(self.image_data):
            # self.glv.move_to_done(self.image_data['path'])
            return

    def stop(self) -> None:
        self._running = False

    def is_running(self) -> bool:
        return self._running
