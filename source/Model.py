from WorldObjects.Player import *
from WorldObjects.Platform import *
from Collisions.collision import *


class Model:
    """
    In the architecture MVC (Model View Controller), Model is the Model.
    So it's one of the greatest and more high-level class.

    Model must manage all the in-game elements, and how they interact each other.

    The classes used by Model must have an `update` method and a `draw` method.
    The `update` method must update the values of the object using the inputs of the player.
    """
    def __init__(self):
        self.__fixes = []
        self.__movables = []
        self.__worldObjects = []
        self.player = self.add_world_object(Player(Vec(0, 100)))
        self.add_world_object(AxisAlignedPlatform(Vec(0, 200), Vec(95, 10)))
        self.add_world_object(AxisAlignedPlatform(Vec(100, 195), Vec(100, 1)))
        self.add_world_object(Platform([Vec(200, 200), Vec(400, 0), Vec(300, 200)]))

# update ---------------------------------------------------------------------------------------------------------------
    def update(self, inputs):
        for world_object in self.__worldObjects:
            world_object.update(inputs)
        resolve_collisions(self.__fixes, self.__movables)

# hitboxes management --------------------------------------------------------------------------------------------------
    def add_hitbox(self, hitbox):
        if hitbox.fix:
            self.__fixes.append(hitbox)
        else:
            self.__movables.append(hitbox)

    def remove_hitbox(self, hitbox):
        if hitbox.fix:
            self.__fixes.remove(hitbox)
        else:
            self.__movables.remove(hitbox)

    @property
    def hitboxes(self):
        return self.__fixes + self.__movables

# WorldObject management -----------------------------------------------------------------------------------------------

    def add_world_object(self, world_object):
        self.__worldObjects.append(world_object)
        for hitbox in world_object.get_hitboxes():
            self.add_hitbox(hitbox)
        return world_object
