from os import rename, path

from bitpandaCalls import BitpandaCalls
from imageHandler import ImageHandler
from predictor import Predictor
from threadManager import ThreadManager
from exchangeManager import ExchangeManager

DEFAULT_CURRENCY = 'EUR'
ACTION_IMAGES_PATH = './../action_images'
DONE_PATH = './../done'
KERAS_MODEL_PATH = './../keras_model'
TRAINING_DATA_PATH = './../../TrainingData/data'
LABEL_FOLDERS = ['no']

PREDICTION_BUY = 'BUY'
PREDICTION_SELL = 'SELL'
PREDICTION_NONE = 'NONE'


class Globalvar:

    def __init__(self):
        self.private = self.get_private_data()
        self.coins = self.currencies()
        self.coin_prices = {}
        self.price_update_time = None

        self.bitpanda = BitpandaCalls(self)
        self.image_handler = ImageHandler(self)
        self.predictor = Predictor(self)
        self.thread_manager = ThreadManager(self)
        self.exchange_manager = ExchangeManager(self)

    def get_private_data(self) -> dict:
        return {
            'key': self.get_key()
        }

    @staticmethod
    def get_key() -> str:
        f = open('../key', 'r')

        return f.read()

    def get_bitpanda_calls(self) -> BitpandaCalls:
        return self.bitpanda

    def get_image_handler(self) -> ImageHandler:
        return self.image_handler

    def get_predictor(self) -> Predictor:
        return self.predictor

    def get_exchange_manager(self) -> ExchangeManager:
        return self.exchange_manager

    def get_thread_manager(self) -> ThreadManager:
        return self.thread_manager

    def coin_order(self, coins_data):
        coins = {}
        for coin in self.coins:
            if coin in self.coins:
                coins[coin] = coins_data[coin]
            else:
                coins[coin] = {'EUR': 1.0}

        return coins

    def set_coin_prices(self, coin_prices: dict) -> None:
        self.coin_prices = coin_prices

    def get_coin_prices(self) -> dict:
        return self.coin_prices

    def set_price_update_time(self, price_update_time):
        self.price_update_time = price_update_time

    def get_price_update_time(self):
        return self.price_update_time

    @staticmethod
    def move_to_done(file_path) -> None:
        file_name = file_path.split('/')[-1]
        if path.isfile(file_path):
            rename(file_path, f'{DONE_PATH}/{file_name}')
        else:
            print(f'File: {file_path} does not exist.')

    @staticmethod
    def move_file(file_path) -> None:
        rename(file_path, f'{ACTION_IMAGES_PATH}/{file_path}')

    @staticmethod
    def currencies() -> list:
        return [
            'XAU',     # 0
            'XAG',     # 1
            'USDC',    # 2
            'PAN',     # 3
            'BTC',     # 4
            'ETH',     # 5
            'USDT',    # 6
            'BNB',     # 7
            'XRP',     # 8
            'ADA',     # 9
            'SOL',     # 10
            'AVAX',    # 11
            'DOT',     # 12
            'DOGE',    # 13
            'XPD',     # 14
            'SHIB',    # 15
            'MATIC',   # 16
            'LTC',     # 17
            'NEAR',    # 18
            'ATOM',    # 19
            'XPT',     # 20
            'LINK',    # 21
            'UNI',     # 22
            'BCH',     # 23
            'FTT',     # 24
            'TRX',     # 25
            'ETC',     # 26
            'ALGO',    # 27
            'XLM',     # 28
            'MANA',    # 29
            'HBAR',    # 30
            'AXS',     # 31
            'ICP',     # 32
            'EGLD',    # 33
            'SAND',    # 34
            'VET',     # 35
            'APE',     # 36
            'FIL',     # 37
            'WAVES',   # 38
            'FTM',     # 39
            'THETA',   # 40
            'KLAY',    # 41
            'XTZ',     # 42
            'ZEC',     # 43
            'EOS',     # 44
            'FLOW',    # 45
            'AAVE',    # 46
            'MIOTA',   # 47
            'GRT',     # 48
            'CAKE',    # 49
            'MKR',     # 50
            'BTT',     # 51
            'ONE',     # 52
            'STX',     # 53
            'GALA',    # 54
            'NEO',     # 55
            'ENJ',     # 56
            'LRC',     # 57
            'DASH',    # 58
            'KSM',     # 59
            'CELO',    # 60
            'BAT',     # 61
            'CHZ',     # 62
            'CRV',     # 63
            'MINA',    # 64
            'AR',      # 65
            'XEM',     # 66
            'XYM',     # 67
            'COMP',    # 68
            'QTUM',    # 69
            'YFI',     # 70
            'OMG',     # 71
            'RVN',     # 72
            '1INCH',   # 73
            'RNDR',    # 74
            'ANKR',    # 75
            'SNX',     # 76
            'KNC',     # 77
            'UMA',     # 78
            'IMX',     # 79
            'ZRX',     # 80
            'IOST',    # 81
            'ONT',     # 82
            'XDB',     # 83
            'SUSHI',   # 84
            'STORJ',   # 85
            'SRM',     # 86
            'REN',     # 87
            'FLUX',    # 88
            'DGB',     # 89
            'OCEAN',   # 90
            'DYDX',    # 91
            'LSK',     # 92
            'BEST',    # 93
            'COTI',    # 94
            'ALICE',   # 95
            'RSR',     # 96
            'ANT',     # 97
            'OXT',     # 98
            'BICO',    # 99
            'REP',     # 100
            'BAND',    # 101
            'DUSK',    # 102
            'KMD',     # 103
            'BCI5',    # 104
            'BCI10',   # 105
            'BCI25',   # 106
            'LUNA',    # 107
        ]
