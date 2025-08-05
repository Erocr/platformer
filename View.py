from Vec import *
import pygame as pg


class View:
    """
    In the architecture MVC (Model View Controller), View is the View.
    So it's one of the greatest and more high-level class.

    View must manage all the outputs of the game, like what is seen on screen, audio, ...

    Warning: think to call flip to show on the screen the differences
    """

    SCREEN_SIZE = Vec(600, 600)

    def __init__(self):
        self.screen = pg.display.set_mode(self.SCREEN_SIZE.get(), pg.RESIZABLE)

    def flip(self):
        """ You must execute this function once you have draw all. It shows the modifications on the screen."""
        pg.display.flip()

    def rect(self, pos_top_left, size, color=(255, 255, 255), border_size=-1):
        """ Draws a rectangle """
        pg.draw.rect(self.screen, color, pg.Rect(pos_top_left.get(), size.get()), width=border_size)
