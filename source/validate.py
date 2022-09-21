import asyncio


class Validate:

    def __init__(self, glv):
        self.glv = glv
        self.bitpanda = glv.get_bitpanda_calls()

    """ Validate by price """
    @staticmethod
    def by_price_and_old_price(price: float, old_price: float) -> bool:
        # Price must have risen by 0.03%
        if price > (old_price * 1.03):
            return True
        return False

    @staticmethod
    def by_balance_and_current_price(balance, current_price) -> bool:
        if balance['available'] * current_price > 1:
            return True
        return False

    """ Validate by price coin and currency """
    def by_price_coin(self, old_price, coin) -> bool:
        current_price = self.glv.get_coin_prices()[coin]

        print(f'Coin: {coin},', f'Image: {old_price},', f'Current: {current_price}')
        if not self.by_price_and_old_price(current_price, old_price):
            return False

        # loop = asyncio.get_event_loop()
        # balance = loop.run_until_complete(self.bitpanda.get_balances(coin))

        # print(f'Coin: {balance["currency_code"]}, Balance: {balance["available"]}')
        # if not self.by_balance_and_current_price(balance, current_price):
        #     return False

        # self.close_loop(loop)
        return True

    def close_loop(self, loop):
        loop.run_until_complete(self.bitpanda.close_client())
