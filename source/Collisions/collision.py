from typing import Optional
from Collisions.Hitbox import *


def all_fixes(hitboxes):
    for h in hitboxes:
        if not h.fix:
            return False
    return True


def all_movables(hitboxes):
    for h in hitboxes:
        if h.fix:
            return False
    return True


def resolve_collision(hitbox1, hitbox2):
    """ It supposes that hitbox2 can't be fix """
    if isinstance(hitbox1, ConvexPolygon) and isinstance(hitbox2, ConvexPolygon):
        ds = poly_poly_collision_dir(hitbox1, hitbox2)
        if ds is not None:
            d1, d2 = ds
            if hitbox1.fix:
                hitbox2.move(-d1+d2)
            else:
                hitbox1.move(d1)
                hitbox2.move(d2)


def resolve_collisions(fixes_hitboxes, movable_hitboxes):
    assert all_fixes(fixes_hitboxes), "fixes_hitboxes must be fixes"
    assert all_movables(movable_hitboxes), "movable_hitboxes must not be fixes"
    for i1 in range(len(fixes_hitboxes)):
        for i2 in range(len(movable_hitboxes)):
            resolve_collision(fixes_hitboxes[i1], movable_hitboxes[i2])
    for i1 in range(len(movable_hitboxes)-1):
        for i2 in range(i1+1, len(movable_hitboxes)):
            resolve_collision(movable_hitboxes[i1], movable_hitboxes[i2])


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
    direction = SAT(p1.points, p2.points)
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
        axe = axe.normalize()
        m1, M1 = project(points1, axe)
        m2, M2 = project(points2, axe)
        if m1 > M2 or m2 > M1:
            return None
        if M2 - m1 > M1 - m2:
            d = m2 - M1
        else:
            d = M2 - m1
        if min_dist is None or abs(d) < min_dist:
            min_dist = abs(d)
            min_dir = axe * d
    return min_dir


def project(points, axe):
    """ Returns the min and max positions of the projection of the points on the axe """
    T = [point.project(axe) for point in points]
    return min(T), max(T)
