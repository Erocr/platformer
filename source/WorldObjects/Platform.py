from WorldObjects.WorldObject import *
from Collisions.Hitbox import *


class AxisAlignedPlatform(WorldObject):
    def __init__(self, pos, size):
        """
        :param pos: the position top left of the platform
        :param size: the size Vec(width, height)
        """
        super().__init__()
        hitbox = Rectangle(pos, size, True)
        self.connect_hitbox(hitbox, both_sides=True)


class Platform(WorldObject):
    def __init__(self, points: list[Vec]):
        """
        :param points: a list of points. Must be convex
        """
        super().__init__()
        hitbox = ConvexPolygon(points)
        self.connect_hitbox(hitbox, both_sides=True)
