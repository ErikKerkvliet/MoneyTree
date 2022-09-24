import numpy as np

from keras.models import load_model
from PIL import Image, ImageOps


class Predictor:

    def __init__(self, glv):
        self.glv = glv
        self.image = None
        self.model = self.load_model()

    @staticmethod
    def load_model():
        return load_model('../keras_model/keras_modal.h5')

    @staticmethod
    def load_image(image_path):
        image = Image.open(image_path)

        size = (224, 224)
        return ImageOps.fit(image, size, Image.ANTIALIAS)

    def load_image_data(self, image_path):
        image = self.load_image(image_path)

        image_array = np.asarray(image)

        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        data[0] = normalized_image_array

        return data

    def predict(self, image_path):
        image_data = self.load_image_data(image_path)

        return self.model.predict(image_data)
