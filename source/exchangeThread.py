import threading

from exchangeHandler import ExchangeHandler


class ExchangeThread(threading.Thread):
    def __init__(self, glv, exchange_type, image_data):
        threading.Thread.__init__(self)
        self._running = True
        self.glv = glv
        self.exchange_type = exchange_type
        self.image_data = image_data

    def run(self):
        return ExchangeHandler(self).start(self.image_data)

    def stop(self):
        self._running = False

    def is_running(self) -> bool:
        return self._running
