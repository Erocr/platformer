from source.Vec import *


class Hitbox:
    def move(self, v):
        pass

    @property
    def pos_top_left(self):
        return Vec(0, 0)


class ConvexPolygon(Hitbox):
    """ It is a hitbox with the shape of a convex polygon """
    def __init__(self, points: list[Vec]):
        self.points = points
        assert len(self.points) >= 3, "A polygon must have at least 3 vertices"
        assert self.__is_convex(), "ConvexPolygon shall be a convex polygon !"
        self.__pos_top_left = sum(self.points) / len(self.points)

    def __is_convex(self) -> bool:
        direction = (self.points[-1] - self.points[-2]).at_his_right(self.points[0] - self.points[-1])
        for i in range(1, len(self.points)-1):
            v1 = self.points[i-1] - self.points[i-2]
            v2 = self.points[i] - self.points[i-1]
            if v1.at_his_right(v2) ^ direction:  # ^ est le xor, (a ^ b) revient à faire (a != b)
                return False
        return True

    @property
    def pos_top_left(self):
        return self.__pos_top_left

    def move(self, v):
        self.__pos_top_left += v
        for i in range(len(self.points)):
            self.points[i] += v


def Rectangle(pos_top_left, size) -> ConvexPolygon:
    points = [
        pos_top_left,
        pos_top_left + Vec(size.x, 0),
        pos_top_left + size,
        pos_top_left + Vec(0, size.y)
    ]
    return ConvexPolygon(points)
