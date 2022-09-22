from globalvar import ACTION_IMAGES_PATH
from globalvar import DONE_PATH

from os import path, makedirs


class Make:

    def __init__(self):
        self.directories()

    @staticmethod
    def directories():
        if not path.isdir(ACTION_IMAGES_PATH):
            makedirs(ACTION_IMAGES_PATH)

        if not path.isdir(DONE_PATH):
            makedirs(DONE_PATH)
