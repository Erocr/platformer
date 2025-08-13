from Math.Vec import *


class Drawable:
    """
    It's an interface for the objects that can be drawn.
    """
    speed = Vec(0, 0)

    def draw(self, drawer):
        assert False, "You forgot to implement the draw function"
