from PIL import Image


class HandleImage:

    def __init__(self, glv):
        self.glv = glv

    def extract_data(self, path) -> None:
        image = Image.open(path)
        pixels = image.load()

        extra_data = []
        exchange_type_id = 0
        last_pixel = image.size[0] - 1
        extra_pixel = 108
        price_start = 10
        for i in range(last_pixel):
            if pixels[last_pixel, i] != 0:
                self.glv.set_coin(i)
                exchange_type_id = pixels[last_pixel, i]
            extra_data.append(pixels[i, extra_pixel])
        print(extra_data)

        price_string = ''
        for i in range(price_start, last_pixel):
            if i == 25:
                break
            char = str(extra_data[i])
            if char == '255':
                char = '.'
            price_string += char
        price = float(''.join(price_string))

        self.glv.set_price(price)
        self.glv.set_extra_data(extra_data)
        self.glv.set_order_data(exchange_type_id)
