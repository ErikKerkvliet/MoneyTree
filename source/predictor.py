import numpy as np
import globalvar

from keras.models import load_model
from PIL import Image, ImageOps


class Predictor:

    def __init__(self, glv=None):
        self.glv = glv
        self.image = None
        self.model = self.load_model()
        # self.predict("/home/erik/PycharmProjects/TrainingData/data/images_50/no/23-09-2022 01:04:25_DOT.png")

    @staticmethod
    def load_model():
        return load_model('../keras_model/keras_model.h5', compile=False)

    @staticmethod
    def load_image(image_path):
        return Image.open(image_path).convert('L')

        size = (224, 224)
        return ImageOps.fit(image, size)

    def load_image_data(self, image_path):
        image = self.load_image(image_path)
        image_array = np.array(image)
        # image_array = np.asarray(image)

        # normalized_image_array = (image.astype(np.float32) / 127.0) - 1

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.uint8)

        # data[0] = normalized_image_array

        return data

    def predict(self, image_path):
        image_data = self.load_image_data(image_path)

        prediction = self.model.predict(image_data)
        predictions = prediction[0].tolist()
        # print(predictions)
        if predictions[0] > predictions[1] < 0.5 and predictions[0] > 0.85:
            return globalvar.PREDICTION_BUY
        elif predictions[1] > predictions[0] < 0.5 and predictions[1] > 0.85:
            return globalvar.PREDICTION_SELL
        else:
            return globalvar.PREDICTION_NONE
