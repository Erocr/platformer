from View.Drawable import *


class Hitbox(Drawable):
    """
    A Hitbox have a speed.
    You must move the Hitbox changing the speed, otherwise there will be some collision problems.
    Be very careful when you teleport the Hitbox, if it teleports in a wall, it could be stuck.

    You can connect a hitbox to a WorldObject. So, when you move the hitbox, it moves the worldObject too.
    """
    def __init__(self, fix=True):
        self.__fix = fix  # Must not be changed after creation !!
        self.worldObjectsConnected = []
        self.speed = Vec(0, 0)
        self.collisionInfos = []

# getter ---------------------------------------------------------------------------------------------------------------

    @property
    def fix(self):
        return self.__fix

# virtual methods ------------------------------------------------------------------------------------------------------

    def move(self, v, who_wants=None, with_collision_control=True):
        if not with_collision_control:
            for worldObject in self.worldObjectsConnected:
                if who_wants != worldObject:
                    worldObject.move(v, who_wants=self)
        else:
            self.speed += v

    def draw(self, drawer):
        assert False, "forgot to implement the draw function !"

# resets ---------------------------------------------------------------------------------------------------------------

    def pre_collision_reset(self):
        """ Must be called before the collision """
        self.collisionInfos = []

# world objects management ---------------------------------------------------------------------------------------------

    def connect_world_object(self, world_object, both_sides=False):
        self.worldObjectsConnected.append(world_object)
        if both_sides:
            world_object.connect_hitbox(self)

    def disconnect_world_object(self, world_object, both_sides=False):
        self.worldObjectsConnected.remove(world_object)
        if both_sides:
            world_object.disconnect_hitbox(self)

    def is_connected_with(self, world_object):
        return world_object in self.worldObjectsConnected

# collisionInfos management --------------------------------------------------------------------------------------------
    def add_collision_info(self, coll_info):
        if coll_info is not None:
            self.collisionInfos.append(coll_info)

# ----------------------------------------------------------------------------------------------------------------------
# Hitboxes examples ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class ConvexPolygon(Hitbox):
    """ It is a hitbox with the shape of a convex polygon """
    def __init__(self, points: list[Vec], fix=True):
        super().__init__(fix)
        self.points = points
        assert len(self.points) >= 3, "A polygon must have at least 3 vertices"
        assert self.__is_convex(), "ConvexPolygon shall be a convex polygon !"

    def __is_convex(self) -> bool:
        direction = (self.points[-1] - self.points[-2]).at_his_right(self.points[0] - self.points[-1])
        for i in range(1, len(self.points)-1):
            v1 = self.points[i-1] - self.points[i-2]
            v2 = self.points[i] - self.points[i-1]
            if v1.at_his_right(v2) ^ direction:  # ^ est le xor, (a ^ b) revient à faire (a != b)
                return False
        return True

    def move(self, v, who_wants=False, with_collision_control=True):
        """
        It moves the hitbox of v. It also moves all his connected world objects.

        :param v: The vector describing the movement
        :param who_wants: which class did call this function. It is used in order to prevent infinite loops.
        In fact, this function calls the move function of worldObjects, which move all the connected hitboxes.
        :param with_collision_control: It must not be disabled, unless you want it to teleport, or it is used in the
        collision's functions.
        """
        super().move(v, who_wants, with_collision_control)
        if not with_collision_control:
            for i in range(len(self.points)):
                self.points[i] += v

    def draw(self, drawer):
        drawer.draw_convex_polygon(self)


def Rectangle(pos_top_left: Vec, size: Vec, fix=True) -> ConvexPolygon:
    """
    An axis aligned rectangle.
    """
    points = [
        pos_top_left,
        pos_top_left + Vec(size.x, 0),
        pos_top_left + size,
        pos_top_left + Vec(0, size.y)
    ]
    return ConvexPolygon(points, fix)
