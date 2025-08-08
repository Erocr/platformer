from Vec import *
from WorldObjects.WorldObject import *
from Collisions.Hitbox import Rectangle


class Player(WorldObject):
    def __init__(self, pos):
        super().__init__()
        hitbox = Rectangle(pos, Vec(30, 30), False)
        self.connect_hitbox(hitbox, both_sides=True)

    def update(self, inputs):
        self.move(Vec(0, 1))
