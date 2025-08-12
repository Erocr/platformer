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
        return 0, d
    else:
        m = d/2
        return m, m


def poly_poly_collision_dir(points1, points2, speed):
    """ How much we shall move points1 so that points1 and points2 are no more in collision """
    max_t = 0

    # POV of points1
    segments = [(points1[i], points1[i] - speed) for i in range(len(points2))]
    for segment in segments:
        for i in range(len(points2)):
            intersection = segment_segment_intersection_t_u(*segment, points2[i - 1], points2[i])
            if intersection is not None:
                t, u = intersection
                if t > max_t:
                    max_t = t

    # POV of points2
    segments = [(points2[i], points2[i]+speed) for i in range(len(points2))]
    for segment in segments:
        for i in range(len(points1)):
            intersection = segment_segment_intersection_t_u(*segment, points1[i-1], points1[i])
            if intersection is not None:
                t, u = intersection
                if t > max_t:
                    max_t = t
    return max_t


def resolve_collision(hitbox1, hitbox2, speed):
    """
    Returns the movement for hitbox1 and for hitbox2 so that they are no more in collision
    It supposes that hitbox2 can't be fix
    """
    d = 0
    if isinstance(hitbox1, ConvexPolygon) and isinstance(hitbox2, ConvexPolygon):
        d = poly_poly_collision_dir(hitbox1.points, hitbox2.points, speed)
    else:
        assert False, f"collisions for {type(hitbox1)} and {type(hitbox2)} has not been implemented"
    if d > 1:
        d = 1
    if d != 0:
        d += 0.0001
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

