from View.Drawable import *


class WorldObject(Drawable):
    """
    A WorldObject is an object in the game world.

    It can have be connected with a hitbox (optional) in order to have collisions
    """
    def __init__(self):
        self.__connected_hitboxes = []

# virtual methods ------------------------------------------------------------------------------------------------------

    def update(self, inputs):
        pass

# movement methods -----------------------------------------------------------------------------------------------------

    def move(self, v: Vec, who_wants=None, with_collision_control=True):
        """
        It moves the world object of v. It also moves all his connected hitboxes.

        :param v: The vector describing the movement
        :param who_wants: which class did call this function. It is used in order to prevent infinite loops.
        In fact, this function calls the move function of hitboxes, which move all the connected worldObjects.
        :param with_collision_control: It must not be disabled, unless you want it to teleport, or it is used in the
        collision's functions.
        """
        for hitbox in self.__connected_hitboxes:
            if hitbox != who_wants:
                hitbox.move(v, who_wants=self)

# Hitbox management ----------------------------------------------------------------------------------------------------

    def connect_hitbox(self, hitbox, both_sides=False):
        self.__connected_hitboxes.append(hitbox)
        if both_sides:
            hitbox.connect_world_object(self)

    def disconnect_hitbox(self, hitbox, both_sides=False):
        self.__connected_hitboxes.remove(hitbox)
        if both_sides:
            hitbox.disconnect_world_object(self)

    def is_connected_with(self, hitbox):
        return hitbox in self.__connected_hitboxes

    def get_hitboxes(self):
        return self.__connected_hitboxes

