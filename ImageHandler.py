from Vec import *
import pygame as pg
import os

IMAGE_EXTENSIONS = ("png", "jpg", "jpeg")


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
        self.__images: dict[str, Image] = {}
        self.factor = Vec(1, 1)

    def get_image(self, image) -> pg.Surface:
        """
        It returns the image associated to `image`.
        If it doesn't exist, it loads the image.
        It also extends the timer in order to keep the image more time in memory.
        """
        if image in self.__images:
            self.__images[image].increment_timer()
            return self.__images[image].im
        else:
            self.__images[image] = Image(image)
            return self.__images[image].im


class Image:
    TIME_INACTION_MAX = 30

    def __init__(self, file_path: str, factor=Vec(1, 1), with_extension=False):
        file_path = 'images/' + file_path
        if not with_extension:
            file_path = file_path + "." + self.__find_extension(file_path)

        self.raw = pg.image.load(file_path)
        self.im = None
        self.im: pg.Surface
        self.resize(factor)

        self.increment_timer()

    def must_be_destroyed(self) -> bool:
        pass

    def increment_timer(self):
        pass

    def resize(self, factor: Vec):
        self.im = pg.transform.scale_by(self.raw, factor.get())

    @staticmethod
    def __find_extension(file_path):
        path_split = file_path.split("/")
        directory = "/".join(path_split[:-1])  # file_path jusqu'au dernier /
        file = path_split[-1]
        files = os.listdir(directory)
        for extension in IMAGE_EXTENSIONS:
            if file + "." + extension in files:
                return extension
        raise FileNotFoundError(f"aucune extension trouvée pour {file_path}. {IMAGE_EXTENSIONS} ont été testés")
