from os import rename, path

from bitpandaCalls import BitpandaCalls
from imageHandler import ImageHandler
from predictor import Predictor
from threadManager import ThreadManager
from exchangeManager import ExchangeManager

DEFAULT_CURRENCY = 'EUR'
ACTION_IMAGES_PATH = './../action_images'
DONE_PATH = './../done'
KERAS_MODEL_PATH = '../keras_models/model'
TRAINING_DATA_PATH = './../../TrainingData/data'
LABEL_FOLDERS = ['yes_plus']

PREDICTION_BUY = 'BUY'
PREDICTION_SELL = 'SELL'
PREDICTION_NONE = 'NONE'

TESTING = True


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
        self.balance = 0.0
        self.test_balances = {}
        self.start_test()

    def start_test(self):
        self.test_balances['EUR'] = 100
        for coin in self.coins:
            self.set_test_balance(coin, 0)

    def get_private_data(self) -> dict:
        return {
            'key': self.get_key()
        }

    def add_balance(self, balance) -> None:
        self.balance += balance

    def get_balance(self) -> float:
        return self.balance

    def add_test_balance(self, coin, balance) -> None:
        self.test_balances[coin] += balance

    def set_test_balance(self, coin=None, balance=None) -> None:
        if coin and balance is not None:
            self.test_balances[coin] = balance
        if coin is None:
            self.test_balances = balance

    def get_test_balance(self, coin=None) -> dict:
        if coin:
            return self.test_balances[coin]
        return self.test_balances

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

    def get_coin_prices(self, coin=None) -> dict:
        if coin:
            return self.coin_prices[coin]
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
            'XAU',      # 0
            'BTC',      # 1
            'ETH',      # 2
            'USDT',     # 3
            'USDC',     # 4
            'XAG',      # 5
            'BNB',      # 6
            'XRP',      # 7
            'ADA',      # 8
            'XPD',      # 9
            'SOL',      # 10
            'DOGE',     # 11
            'DOT',      # 12
            'XPT',      # 13
            'MATIC',    # 14
            'SHIB',     # 15
            'TRX',      # 16
            'AVAX',     # 17
            'UNI',      # 18
            'LINK',     # 19
            'LTC',      # 20
            'ETC',      # 21
            'ATOM',     # 22
            'FTT',      # 23
            'XLM',      # 24
            'NEAR',     # 25
            'ALGO',     # 26
            'BCH',      # 27
            'FLOW',     # 28
            'LUNC',     # 29
            'FIL',      # 30
            'APE',      # 31
            'QNT',      # 32
            'ICP',      # 33
            'VET',      # 34
            'ETHW',     # 35
            'HBAR',     # 36
            'MANA',     # 37
            'XTZ',      # 38
            'CHZ',      # 39
            'SAND',     # 40
            'EOS',      # 41
            'EGLD',     # 42
            'THETA',    # 43
            'XVS',      # 44
            'AAVE',     # 45
            'AXS',      # 46
            'OKB',      # 47
            'ZEC',      # 48
            'MIOTA',    # 49
            'BTT',      # 50
            'MKR',      # 51
            'CAKE',     # 52
            'HT',       # 53
            'GRT',      # 54
            'HNT',      # 55
            'NEO',      # 56
            'KLAY',     # 57
            'FTM',      # 58
            'SNX',      # 59
            'RUNE',     # 60
            'CRV',      # 61
            'GT',       # 62
            'ENJ',      # 63
            'DASH',     # 64
            'BAT',      # 65
            'COMP',     # 66
            'STX',      # 67
            'KAVA',     # 68
            'WAVES',    # 69
            'RVN',      # 70
            'MINA',     # 71
            'LRC',      # 72
            'GMT',      # 73
            'TWT',      # 74
            'CELO',     # 75
            'XEM',      # 76
            'DCR',      # 77
            'KSM',      # 78
            'ZIL',      # 79
            'RSR',      # 80
            '1INCH',    # 81
            'BNX',      # 82
            'ENS',      # 83
            'LUNA',     # 84
            'GNO',      # 85
            'AR',       # 86
            'ANKR',     # 87
            'YFI',      # 88
            'GALA',     # 89
            'QTUM',     # 90
            'KDA',      # 91
            'IOTX',     # 92
            'GLM',      # 93
            'ONE',      # 94
            'OMG',      # 95
            'POLY',     # 96
            'ZRX',      # 97
            'FLUX',     # 98
            'ICX',      # 99
            'LPT',      # 100
            'JST',      # 101
            'IOST',     # 102
            'WEMIX',    # 103
            'OP',       # 104
            'KNC',      # 105
            'SRM',      # 106
            'XYM',      # 107
            'ONT',      # 108
            'STORJ',    # 109
            'WAXP',     # 110
            'SC',       # 111
            'MXC',      # 112
            'GLMR',     # 113
            'ZEN',      # 114
            'CSPR',     # 115
            'IMX',      # 116
            'SXP',      # 117
            'AUDIO',    # 118
            'UMA',      # 119
            'WOO',      # 120
            'SCRT',     # 121
            'PLA',      # 122
            'DGB',      # 123
            'SKL',      # 124
            'SUSHI',    # 125
            'ASTR',     # 126
            'CVC',      # 127
            'CKB',      # 128
            'PUNDIX',   # 129
            'LSK',      # 130
            'BEST',     # 131
            'COTI',     # 132
            'RNDR',     # 133
            'REN',      # 134
            'ORBS',     # 135
            'SYS',      # 136
            'CELR',     # 137
            'REQ',      # 138
            'XNO',      # 139
            'SNT',      # 140
            'OCEAN',    # 141
            'LOOKS',    # 142
            'POWR',     # 143
            'CTSI',     # 144
            'BNT',      # 145
            'DYDX',     # 146
            'BICO',     # 147
            'SANTOS',   # 148
            'RAY',      # 149
            'C98',      # 150
            'REP',      # 151
            'EUROC',    # 152
            'CTK',      # 153
            'STRAX',    # 154
            'STMX',     # 155
            'MTL',      # 156
            'JOE',      # 157
            'RAD',      # 158
            'STPT',     # 159
            'OXT',      # 160
            'LOOM',     # 161
            'FXS',      # 162
            'ANT',      # 163
            'VTHO',     # 164
            'NKN',      # 165
            'FET',      # 166
            'ACH',      # 167
            'EFI',      # 168
            'ALICE',    # 169
            'SUPER',    # 170
            'AERGO',    # 171
            'UTK',      # 172
            'PERP',     # 173
            'MBL',      # 174
            'DUSK',     # 175
            'TT',       # 176
            'BAKE',     # 177
            'SUN',      # 178
            'PORTO',    # 179
            'BAND',     # 180
            'TOMO',     # 181
            'ARPA',     # 182
            'YGG',      # 183
            'MLN',      # 184
            'SFP',      # 185
            'AVA',      # 186
            'ILV',      # 187
            'WAN',      # 188
            'KMD',      # 189
            'TROY',     # 190
            'LINA',     # 191
            'AKT',      # 192
            'TRU',      # 193
            'TVK',      # 194
            'BLZ',      # 195
            'PSG',      # 196
            'IRIS',     # 197
            'FARM',     # 198
            'GTC',      # 199
            'CHESS',    # 200
            'BAR',      # 201
            'PAN',      # 202
            'CITY',     # 203
            'AGLD',     # 204
            'HIGH',     # 205
            'QUICK',    # 206
            'VOXEL',    # 207
            'DODO',     # 208
            'ATM',      # 209
            'JUV',      # 210
            'XDB',      # 211
            'XRT',      # 212
            'BCI5',     # 213
            'BCI10',    # 214
            'BCI25',    # 215
            'BCISL',    # 216
            'BCIIL',    # 217
            'BCIDL',    # 218
            'BCIML',    # 219
        ]
