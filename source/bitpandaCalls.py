import json
from datetime import datetime

from bitpanda.BitpandaClient import BitpandaClient
# from bitpanda.subscriptions import MarketTickerSubscription
from exceptions import CoinIndexNotFoundException, CurrencyIndexNotFoundException
import http.client
from bitpanda.enums import TimeUnit
from bitpanda.Pair import Pair


class BitpandaCalls:

    def __init__(self, glv):
        self.glv = glv
        self.client = BitpandaClient(self.glv.private['key'])

    async def get_currencies(self, coin='all'):
        response = await self.client.get_currencies()

        if coin == 'all':
            print(response['response'])
            return response['response']

        for coin_data in response['response']:
            if coin_data['code'] == coin:
                print(coin_data)
                return coin_data

    async def get_balances(self, coin='all'):
        response = await self.client.get_account_balances()

        if coin == 'all':
            return response['response']['balances']

        for balance in response['response']['balances']:
            if balance['currency_code'] == coin:
                return balance
        return {}

    async def close_client(self):
        await self.client.close()

    async def coin_specifics(self, coin):
        response = self.client.get_candlesticks(
            Pair(coin, 'EUR'),
            TimeUnit.MINUTES,
            'nu',
            datetime.now(),
            datetime.now()
        )
        print(response)
        exit()

    @staticmethod
    def ticker(coin='ALL', currency='ALL'):
        data = None

        connection = http.client.HTTPSConnection("api.bitpanda.com")
        while data is None:
            try:
                headers = {'Accept': "application/json"}

                connection.request("GET", "/v1/ticker", headers=headers)

                response = connection.getresponse()
                data = response.read()
            except http.client.NotConnected:
                print('Exception: disconnected. \n Reconnect')
                connection = http.client.HTTPSConnection("api.bitpanda.com")
                continue
            except http.client.HTTPException:
                print('Exception: HTTP Exception. \n Reconnect')
                connection = http.client.HTTPSConnection("api.bitpanda.com")
                continue

        response_data = json.loads(data.decode("utf-8"))

        if coin != 'ALL' and coin not in response_data.keys():
            raise CoinIndexNotFoundException

        if coin == 'ALL' and currency != 'ALL':
            coins_data = {}
            for coin in response_data.keys():
                coins_data[coin] = {}
                for currency_code in response_data[coin].keys():
                    coins_data[coin] = float(response_data[coin][currency_code])
            return coins_data

        if coin == 'ALL':
            return response_data

        if currency not in response_data[coin]:
            raise CurrencyIndexNotFoundException

        if currency == 'ALL':
            return response_data[coin]

        return float(response_data[coin][currency])

    # UNI , EURO Koop 2 UNI voor ? EURO
    # side = OrderSide('BUY')
    # pair = Pair('UNI', 'EUR')
    # response = await client.create_market_order(pair, OrderSide.BUY, '2')
    # print(json.dumps(response['response']))
    # UNI , EUR sell 2 UNI voor ? EURO
    # await client.close()
    async def create_order(self, order_data) -> dict:
        return await self.client.create_market_order(
            order_data['pair'],
            order_data['exchange_type'],
            order_data['amount']
        )
