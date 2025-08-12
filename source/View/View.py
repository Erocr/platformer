import pygame as pg
from View.Drawer import Drawer
from Math.Vec import *


class View:
    """
    In the architecture MVC (Model View Controller), View is the View.
    So it's one of the greatest and more high-level class.

    View must manage all the outputs of the game, like what is seen on screen, audio, ...
    He manages them through the function draw taking the model as parameter.

    Warning: think to call flip to show on the screen the differences
    """

    SCREEN_SIZE = Vec(600, 600)

    def __init__(self):
        self.screen = pg.display.set_mode(self.SCREEN_SIZE.get(), pg.RESIZABLE)
        self.drawer = Drawer(self)

    def draw(self, model):
        """ It updates the screen, drawing all the elements in model """
        self.screen.fill((0, 0, 0))
        self.__draw_hitboxes(model)
        self.flip()

    def __draw_hitboxes(self, model):
        """ It draws the hitboxes, you should not use this function if you want to draw images instead """
        for hitbox in model.hitboxes:
            hitbox.draw(self.drawer)

    def flip(self):
        """ You must execute this function once you have draw all. It shows the modifications on the screen."""
        pg.display.flip()

    def draw_rect(self, pos_top_left, size, color=(255, 255, 255), border_size=-1):
        """ Draws a rectangle """
        pg.draw.rect(self.screen, color, pg.Rect(pos_top_left.get(), size.get()), width=border_size)

    def draw_polygon(self, points, color=(255, 255, 255), border_size=0):
        """ Draws a polygon """
        points = [point.get() for point in points]
        pg.draw.polygon(self.screen, color, points, width=border_size)


if __name__ == "__main__":
    view = View()
