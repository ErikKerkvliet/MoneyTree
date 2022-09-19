
EXTRA_PIXEL = 108


class ImageHandler:

    def __init__(self, glv):
        self.glv = glv

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
            extra_data.append(pixels[i][EXTRA_PIXEL])

        return {
            'coin': coin,
            'price': self.get_price(extra_data[10:25]),
            'exchange_type_id': exchange_type_id,
            'wait_time': extra_data[8],
        }

    """ Get coin price """
    @staticmethod
    def get_price(extra_data) -> float:
        price_string = ''
        for char in extra_data:
            if char == 255:
                char = '.'
            price_string += str(char)
        return float(''.join(price_string))
