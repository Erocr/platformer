from typing import Optional
from Collisions.Hitbox import *
from Math.intersections import *


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


def collision_repartition(hitbox1, hitbox2, d):
    """ It supposes that hitbox2 can't be fix """
    if hitbox1.fix:
        return 0, min(d, 1)
    else:
        m = min(d/2, 1)
        return m, m


def resolve_collision(hitbox1, hitbox2, speed):
    """
    Returns the movement for hitbox1 and for hitbox2 so that they are no more in collision
    It supposes that hitbox2 can't be fix
    """
    d = 0
    if isinstance(hitbox1, ConvexPolygon) and isinstance(hitbox2, ConvexPolygon):
        if poly_poly_collision(hitbox1, hitbox2):
            d = poly_poly_collision_on_axe_precise(hitbox1.points, hitbox2.points, speed)
    else:
        assert False, f"collisions for {type(hitbox1)} and {type(hitbox2)} has not been implemented"
    return collision_repartition(hitbox1, hitbox2, d)


def resolve_collisions(fixes_hitboxes, movable_hitboxes):
    """ It moves the hitboxes of their speed, and rewind the time until they are no more in collision """
    assert all_fixes(fixes_hitboxes), "fixes_hitboxes must be fixes"
    assert all_movables(movable_hitboxes), "movable_hitboxes must not be fixes"

    # X coordinate
    movable_rewinds = [0] * len(movable_hitboxes)
    for hitbox in fixes_hitboxes + movable_hitboxes:
        hitbox.move(Vec(hitbox.speed.x, 0), with_collision_control=False)
    for i1 in range(len(fixes_hitboxes)):
        for i2 in range(len(movable_hitboxes)):
            relative_speed = Vec(fixes_hitboxes[i1].speed.x - movable_hitboxes[i2].speed.x, 0)
            d1, d2 = resolve_collision(fixes_hitboxes[i1], movable_hitboxes[i2], relative_speed)
            movable_rewinds[i2] = max(d2, movable_rewinds[i2])
    for i1 in range(len(movable_hitboxes)-1):
        for i2 in range(i1+1, len(movable_hitboxes)):
            relative_speed = Vec(movable_hitboxes[i1].speed.x - movable_hitboxes[i2].speed.x, 0)
            d1, d2 = resolve_collision(movable_hitboxes[i1], movable_hitboxes[i2], relative_speed)
            movable_rewinds[i1] = max(d1, movable_rewinds[i1])
            movable_rewinds[i2] = max(d2, movable_rewinds[i2])
    for i in range(len(movable_hitboxes)):
        hitbox = movable_hitboxes[i]
        d = movable_rewinds[i]
        hitbox.move(Vec(-hitbox.speed.x * d, 0), with_collision_control=False)

    # Y coordinate
    movable_rewinds = [0] * len(movable_hitboxes)
    for hitbox in fixes_hitboxes + movable_hitboxes:
        hitbox.move(Vec(0, hitbox.speed.y), with_collision_control=False)
    for i1 in range(len(fixes_hitboxes)):
        for i2 in range(len(movable_hitboxes)):
            relative_speed = Vec(0, fixes_hitboxes[i1].speed.y - movable_hitboxes[i2].speed.y)
            d1, d2 = resolve_collision(fixes_hitboxes[i1], movable_hitboxes[i2], relative_speed)
            movable_rewinds[i2] = max(d2, movable_rewinds[i2])
    for i1 in range(len(movable_hitboxes) - 1):
        for i2 in range(i1 + 1, len(movable_hitboxes)):
            relative_speed = Vec(0, movable_hitboxes[i1].speed.y - movable_hitboxes[i2].speed.y)
            d1, d2 = resolve_collision(movable_hitboxes[i1], movable_hitboxes[i2], relative_speed)
            movable_rewinds[i1] = max(d1, movable_rewinds[i1])
            movable_rewinds[i2] = max(d2, movable_rewinds[i2])
    for i in range(len(movable_hitboxes)):
        hitbox = movable_hitboxes[i]
        d = movable_rewinds[i]
        hitbox.move(Vec(0, -hitbox.speed.y * d), with_collision_control=False)
        hitbox.speed = Vec(0, 0)


def poly_poly_collision(p1: ConvexPolygon, p2: ConvexPolygon) -> bool:
    """
    Returns if there is a collision between p1 and p2

    It uses the SAT algorithm to find the collision between p1 and p2
    """
    return SAT(p1.points, p2.points) is not None


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
        d = poly_poly_collision_on_axe(points1, points2, axe)
        if d is None: return
        if min_dist is None or abs(d) < min_dist:
            min_dist = abs(d)
            min_dir = axe * d
    return min_dir


def poly_poly_collision_on_axe(points1, points2, axe, must_be_positive=False):
    """
    Returns the amount of movement so that points1 and points2 are no more in collision. The movement is only along the
    axe. The vectorial form of this movement is axe * d (with d the result of the function).

    It supposes that points1 and points2 are in collision.
    """
    if axe == Vec(0, 0):
        return 0
    m1, M1 = project(points1, axe)
    m2, M2 = project(points2, axe)
    if m1 >= M2 or m2 >= M1:
        return None
    if must_be_positive:
        return M2 - m1
    if M2 - m1 > M1 - m2:
        d = m2 - M1
    else:
        d = M2 - m1
    return d


def __find_extremities(points1, points2, speed):
    """ Returns the projection value on the axe perpendicular to speed of the extremities of the smaller polygon """
    axe = speed.rotate90_clockwise()
    m1, M1 = project(points1, axe)
    m2, M2 = project(points2, axe)
    M = min(M1, M2)
    m = max(m1, m2)
    return m, M


def __in_extremities(points, extremity1, extremity2, speed):
    """ Returns the points which are in between extremity1 and extremity2 (extremity1 and extremity2 are lines) """
    axe = speed.rotate90_clockwise()
    L = []
    for point in points:
        if extremity1 <= point.project(axe) <= extremity2:
            L.append(point)
    bigAxe1 = axe * extremity1, axe * extremity1 + speed
    bigAxe2 = axe * extremity2, axe * extremity2 + speed
    for i in range(len(points)):
        intersection1 = segment_line_intersection(points[i-1], points[i], *bigAxe1)
        intersection2 = segment_line_intersection(points[i-1], points[i], *bigAxe2)
        if intersection1 is not None:
            L.append(intersection1)
        if intersection2 is not None:
            L.append(intersection2)
    return L


def poly_poly_collision_on_axe_precise(points1, points2, speed):
    """ returns how much we shall move points1 so that points1 are no more in collision with points2 """
    if speed == Vec(0, 0):
        return 0
    speed = speed.normalize()
    extremities = __find_extremities(points1, points2, speed)
    points1_skim = __in_extremities(points1, *extremities, speed)
    points2_skim = __in_extremities(points2, *extremities, speed)
    m1, M1 = project(points1_skim, speed)
    m2, M2 = project(points2_skim, speed)
    return max(min(M1 - m2, 1), 0)


def project(points, axe):
    """ Returns the min and max positions of the projection of the points on the axe """
    T = [point.project(axe) for point in points]
    return min(T), max(T)
