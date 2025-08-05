from Vec import *
import pygame as pg


class ImageHandler:
    """
    The ImageHandler has the role to load images, and store them.

    He accesses the images in the images directory, and in his subdirectories. You can access to the images using
    their relative path (without the extension).

    The ImageHandler doesn't load all the images at the beginning. He loads only the one you need.
    Then, he puts a timer on each image, and refresh it every time we use the image. If the image is not used for a
    while, it is forgotten.
    """
    def __init__(self):
        self.__images = {}

    def get_image(self, __image) -> pg.Surface:
        """
        It returns the image associated to `image`.
        If it doesn't exist, it loads the image.
        It also extends the timer in order to keep the image more time in memory.
        """
        pass


class Image:
    def __init__(self, file_path: str):
        self.raw = None
        self.im = None
        self.timer = 0

    def must_be_destroyed(self) -> bool:
        pass

    def resize(self, factor: Vec):
        pass
