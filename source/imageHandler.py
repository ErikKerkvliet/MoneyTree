from bitpanda.enums import OrderSide
from PIL import Image


class ImageHandler:

    def __init__(self, glv):
        self.glv = glv

    # noinspection PyUnresolvedReferences
    @staticmethod
    def get_image_pixel_data(path) -> list:
        image = Image.open(path)

        pixels = image.load()
        width, height = image.size
        if width != 224 or height != 224:
            return []

        image_data = []
        for x in range(width):
            image_data.append([])
            for y in range(height):
                pixel = pixels[x, y]
                image_data[x].append(pixel)

        return image_data

    def extract_data(self, image_data: list) -> dict:
        last_pixel = len(image_data) - 1
        return self.extract_extra_data(image_data, last_pixel)

    """ format = [0 => week day, 1-2 => day, 3-4 => month, 5-6 => year, 7 => timer, 8 => result_time, 9-x => price] """
    def extract_extra_data(self, pixels, last_pixel) -> dict:
        coin = ''
        exchange_type_id = 0
        extra_data = []
        for i in range(last_pixel):
            if pixels[last_pixel][i] != 0:
                coin = self.glv.coins[i]
                exchange_type_id = pixels[last_pixel][i]
            extra_data.append(pixels[i][last_pixel])

        return {
            'coin': coin,
            'price': self.get_price(extra_data[10:25]),
            'exchange_type': self.get_action(exchange_type_id),
            'wait_time': extra_data[8],
        }

    """ Get coin price """
    @staticmethod
    def get_price(extra_data) -> float:
        price_string = ''
        for char in extra_data:
            if char == 255:
                char = '.'
            elif char == 254:
                char = 'e'
            elif char == 253:
                char = '-'
            price_string += str(char)
        return float(''.join(price_string))

    @staticmethod
    def get_action(action):
        if action == 255:
            return OrderSide.BUY.value
        elif action == 127:
            return OrderSide.SELL.value
        elif action == 0:
            return False
        else:
            return None
