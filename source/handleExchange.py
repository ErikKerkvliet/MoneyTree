import asyncio
import json
from datetime import datetime

from bitpanda.BitpandaClient import BitpandaClient
import http.client
from bitpanda.enums import TimeUnit
from bitpanda.Pair import Pair


class HandleExchange:

    def __init__(self, glv, exchange_type):
        self.glv = glv
        self.type = exchange_type

        self.connection = http.client.HTTPSConnection("api.bitpanda.com")
        self.headers = {'Accept': "application/json"}
        self.client = BitpandaClient(self.glv.private['key'])
        self.loop = asyncio.get_event_loop()

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

    def ticker(self, coin='ALL', currency='ALL'):
        data = None
        while data is None:
            try:
                self.connection.request("GET", "/v1/ticker", headers=self.headers)

                response = self.connection.getresponse()
                data = response.read()
            except http.client.NotConnected:
                print('Exception: disconnected. \n Reconnect')
                self.connection = http.client.HTTPSConnection("api.bitpanda.com")
                continue
            except http.client.HTTPException:
                print('Exception: HTTP Exception. \n Reconnect')
                self.connection = http.client.HTTPSConnection("api.bitpanda.com")
                continue

        response_data = json.loads(data.decode("utf-8"))
        print(response_data)
        data = self.glv.coin_order(response_data)
        print(data)
        if True:
            for coin in response_data.keys():
                print(self.glv.coin, self.glv.price, coin, response_data[coin]['EUR'])

        return response_data

        if currency == 'ALL':
            return response_data[coin]

        return response_data[coin][currency]

    # UNI , EURO Koop 2 UNI voor ? EURO
    # side = OrderSide('BUY')
    # pair = Pair('UNI', 'EUR')
    # response = await client.create_market_order(pair, OrderSide.BUY, '2')
    # print(json.dumps(response['response']))
    # UNI , EUR sell 2 UNI voor ? EURO
    # await client.close()
    async def create_order(self) -> dict:
        order_data = self.glv.get_order_data()

        return await self.client.create_market_order(order_data['pair'], order_data['type'], order_data['amount'])
