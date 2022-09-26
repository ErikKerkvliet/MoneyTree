import datetime
import threading
import time
import globalvar


class TickerThread(threading.Thread):
    def __init__(self, glv):
        threading.Thread.__init__(self, name='ticker')
        self._running = True
        self.glv = glv
        self.bitpanda = self.glv.get_bitpanda_calls()
        self.glv.set_price_update_time(datetime.datetime.now())
        self.glv.set_coin_prices(self.bitpanda.ticker(currency=globalvar.DEFAULT_CURRENCY))

    def run(self):
        print(f'Start time: {self.glv.get_price_update_time()}')
        while True:

            coin_prices = self.bitpanda.ticker(currency=globalvar.DEFAULT_CURRENCY)
            keys = coin_prices.keys()

            # See if coin in response are all present in self.glv.coins
            # difference = set(self.glv.coins).symmetric_difference(set(keys))
            # if len(list(difference)) > 0:
            #     print("Currency keys don't all match.")
            #     break

            global_coin_prices = self.glv.get_coin_prices()
            for coin in keys:
                if global_coin_prices[coin] != coin_prices[coin]:
                    self.glv.set_price_update_time(datetime.datetime.now())
                    self.glv.set_coin_prices(coin_prices)

                    print(f'Update time: {self.glv.get_price_update_time()}')
                    print(coin_prices['BTC'])
                    break

            time.sleep(1)

        self.stop()
        return

    def stop(self) -> None:
        self._running = False

    def is_running(self) -> bool:
        return self._running
