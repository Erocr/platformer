from typing import Optional

from Hitbox import *


def poly_poly_collision(p1: ConvexPolygon, p2: ConvexPolygon) -> bool:
    """
    Returns if there is a collision between p1 and p2

    It uses the SAT algorithm to find the collision between p1 and p2
    """
    return SAT(p1, p2) is not None


def poly_poly_collision_dir(p1: ConvexPolygon, p2: ConvexPolygon) -> Optional[tuple[Vec, Vec]]:
    """
    if there is no collision, it returns None, else it returns a tuple with the movement to make p1 no more in
    collision with p2, and the movement to make p2 no more in collision with p1

    It uses the SAT algorithm to find the collision between p1 and p2
    """
    direction = SAT(p1, p2)
    if direction is None:
        return None
    else:
        return direction/2, -direction/2


def find_axes(points1, points2):
    """ Find the axes for usage of SAT algorithm """
    res = []
    for points in (points1, points2):
        for i in range(len(points)):
            res.append((points[i] - points[i-1]).rotate90_clockwise())
    return res


def SAT(points1, points2):
    """
    It supposes that axes are the perpendiculars of the segment's directions

    If points1 and points2 collide, it returns the movement for points1 in order to stop collide.
    If they don't collide, it returns None
    """
    axes = find_axes(points1, points2)
    min_dir = None
    min_dist = None
    for axe in axes:
        m1, M1 = project(points1, axe)
        m2, M2 = project(points2, axe)
        if m1 > M2 or m2 > M1:
            return None
        if M2 - m1 > M1 - m2:
            d = m2 - M1
        else:
            d = M2 - m1
        if abs(d) < min_dist:
            min_dist = abs(d)
            min_dir = d * axe
    return min_dir


def project(points, axe):
    """ Returns the min and max positions of the projection of the points on the axe """
    T = [point.project(axe) for point in points]
    return min(T), max(T)
