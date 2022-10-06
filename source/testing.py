import time
import globalvar
from validate import Validate

class Testing:

    def __init__(self, glv):
        self.glv = glv
        self.validate = Validate(self.glv)

    def test(self, extracted):
        old_price = self.glv.get_coin_prices(extracted['coin'])

        if (self.glv.get_coin_prices(globalvar.DEFAULT_CURRENCY) / 100) < 1:
            amount = 1
        else:
            amount = (self.glv.get_coin_prices(globalvar.DEFAULT_CURRENCY) / 100)

        self.glv.add_test_balance(globalvar.DEFAULT_CURRENCY, -amount)
        self.glv.add_test_balance(extracted['coin'], old_price)

        time.sleep(extracted['wait_time'])

        price = self.glv.get_coin_prices()[extracted['coin']]

        if not self.glv.validate.by_price_coin(old_price, price):
            self.glv.add_test_balance(globalvar.DEFAULT_CURRENCY, 0.99)
            self.glv.add_test_balance(extracted['coin'], -old_price)
            return False

        gain = (price - old_price) * 0.97

        self.glv.add_test_balance(globalvar.DEFAULT_CURRENCY, 1.01)
        self.glv.add_test_balance(extracted['coin'], -amount)
        self.glv.add_test_balance(extracted['coin'], gain)

        f = open('result.txt', 'w')

        for coin in self.glv.get_test_balance().keys():
            f.write(f'{coin}: {self.glv.get_test_balance(coin)}\n')

        f.close()
