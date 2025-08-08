from source.Vec import *


class Hitbox:
    """
    A Hitbox have a speed.
    You must move the Hitbox changing the speed, otherwise there will be some collision problems.
    Be very careful when you teleport the Hitbox, if it teleports in a wall, it could be stuck.

    You can connect a hitbox to a WorldObject. So, when you move the hitbox, it moves the worldObject too.
    """
    speed = Vec(0, 0)

    def __init__(self, fix=True):
        self.__fix = fix  # Must not be changed after creation !!
        self.worldObjectsConnected = []

    @property
    def fix(self):
        return self.__fix

    def move(self, v, who_wants=None):
        for worldObject in self.worldObjectsConnected:
            if who_wants != worldObject:
                worldObject.move(v, who_wants=self)

    def draw(self, drawer):
        assert False, "forgot to implement the draw function !"

    def connect_world_object(self, worldObject, both_sides=False):
        self.worldObjectsConnected.append(worldObject)
        if both_sides:
            worldObject.connect_hitbox(self)

    def disconnect_world_object(self, worldObject, both_sides=False):
        self.worldObjectsConnected.remove(worldObject)
        if both_sides:
            worldObject.disconnect_hitbox(self)

    def is_connected_with(self, worldObject):
        return worldObject in self.worldObjectsConnected


class ConvexPolygon(Hitbox):
    """ It is a hitbox with the shape of a convex polygon """
    def __init__(self, points: list[Vec], fix=True):
        super().__init__(fix)
        self.points = points
        assert len(self.points) >= 3, "A polygon must have at least 3 vertices"
        assert self.__is_convex(), "ConvexPolygon shall be a convex polygon !"
        self.__pos_top_left = sum(self.points, start=Vec(0, 0)) / len(self.points)

    def __is_convex(self) -> bool:
        direction = (self.points[-1] - self.points[-2]).at_his_right(self.points[0] - self.points[-1])
        for i in range(1, len(self.points)-1):
            v1 = self.points[i-1] - self.points[i-2]
            v2 = self.points[i] - self.points[i-1]
            if v1.at_his_right(v2) ^ direction:  # ^ est le xor, (a ^ b) revient à faire (a != b)
                return False
        return True

    def move(self, v, who_wants=False):
        if v.y < -800:
            print(v)
        super().move(v, who_wants)
        self.__pos_top_left += v
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
