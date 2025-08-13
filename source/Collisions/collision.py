from typing import Optional
from Collisions.Hitbox import *
from Collisions.CollisionInfo import *
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


def collision_repartition(hitbox1, hitbox2, d) -> tuple[float, float]:
    """ It supposes that hitbox2 can't be fix """
    if hitbox1.fix:
        return 0, d
    else:
        m = d/2
        return m, m


def poly_poly_collision_dir(points1, points2, speed):
    """
    How much we shall move points1 so that points1 and points2 are no more in collision
    It returns the tangent of the collision too
    """
    max_t = 0
    tangent = Vec(0, 0)

    # POV of points1
    segments = [(points1[i], points1[i] - speed) for i in range(len(points2))]
    for segment in segments:
        for i in range(len(points2)):
            intersection = segment_segment_intersection_t_u(*segment, points2[i - 1], points2[i])
            if intersection is not None:
                t, u = intersection
                if t > max_t:
                    max_t = t
                    tangent = points2[i - 1] - points2[i]

    # POV of points2
    segments = [(points2[i], points2[i]+speed) for i in range(len(points2))]
    for segment in segments:
        for i in range(len(points1)):
            intersection = segment_segment_intersection_t_u(*segment, points1[i-1], points1[i])
            if intersection is not None:
                t, u = intersection
                if t > max_t:
                    max_t = t
                    tangent = points1[i-1] - points1[i]
    return max_t, tangent


def resolve_collision(hitbox1, hitbox2, speed) -> tuple[tuple[float, float], Vec]:
    """
    Returns the movement for hitbox1 and for hitbox2 so that they are no more in collision
    It supposes that hitbox2 can't be fix
    It returns the tangent of the collision too
    """
    if isinstance(hitbox1, ConvexPolygon) and isinstance(hitbox2, ConvexPolygon):
        d, t = poly_poly_collision_dir(hitbox1.points, hitbox2.points, speed)
    else:
        assert False, f"collisions for {type(hitbox1)} and {type(hitbox2)} has not been implemented"
    if d > 1:
        d = 1
    if d != 0:
        d += 0.0001
    return collision_repartition(hitbox1, hitbox2, d), t


def resolve_collisions(fixes_hitboxes, movable_hitboxes):
    """ It moves the hitboxes of their speed, and rewind the time until they are no more in collision """
    assert all_fixes(fixes_hitboxes), "fixes_hitboxes must be fixes"
    assert all_movables(movable_hitboxes), "movable_hitboxes must not be fixes"

    for hitbox in fixes_hitboxes + movable_hitboxes: hitbox.pre_collision_reset()

    # X coordinate
    movable_rewinds = [0.0] * len(movable_hitboxes)
    collisions_infos: list[Optional[CollisionInfo]] = [None] * len(movable_hitboxes)
    for hitbox in fixes_hitboxes + movable_hitboxes:
        hitbox.move(Vec(hitbox.speed.x, 0), with_collision_control=False)
    for i1 in range(len(fixes_hitboxes)):
        for i2 in range(len(movable_hitboxes)):
            relative_speed = Vec(fixes_hitboxes[i1].speed.x - movable_hitboxes[i2].speed.x, 0)
            (d1, d2), t = resolve_collision(fixes_hitboxes[i1], movable_hitboxes[i2], relative_speed)
            if movable_rewinds[i2] < d2:
                movable_rewinds[i2] = d2
                collisions_infos[i2] = CollisionInfo(fixes_hitboxes[i1], t)
    for i1 in range(len(movable_hitboxes)-1):
        for i2 in range(i1+1, len(movable_hitboxes)):
            relative_speed = Vec(movable_hitboxes[i1].speed.x - movable_hitboxes[i2].speed.x, 0)
            (d1, d2), t = resolve_collision(movable_hitboxes[i1], movable_hitboxes[i2], relative_speed)
            if movable_rewinds[i2] < d2:
                movable_rewinds[i2] = d2
                collisions_infos[i2] = CollisionInfo(movable_hitboxes[i1], t)
            if movable_rewinds[i1] < d1:
                movable_rewinds[i1] = d1
                collisions_infos[i1] = CollisionInfo(movable_hitboxes[i2], t)
    for i in range(len(movable_hitboxes)):
        hitbox = movable_hitboxes[i]
        d = movable_rewinds[i]
        hitbox.move(Vec(-hitbox.speed.x * d, 0), with_collision_control=False)
        hitbox.add_collision_info(collisions_infos[i])

    # Y coordinate
    movable_rewinds = [0.0] * len(movable_hitboxes)
    collisions_infos: list[Optional[CollisionInfo]] = [None] * len(movable_hitboxes)
    for hitbox in fixes_hitboxes + movable_hitboxes:
        hitbox.move(Vec(0, hitbox.speed.y), with_collision_control=False)
    for i1 in range(len(fixes_hitboxes)):
        for i2 in range(len(movable_hitboxes)):
            relative_speed = Vec(0, fixes_hitboxes[i1].speed.y - movable_hitboxes[i2].speed.y)
            (d1, d2), t = resolve_collision(fixes_hitboxes[i1], movable_hitboxes[i2], relative_speed)
            if movable_rewinds[i2] < d2:
                movable_rewinds[i2] = d2
                collisions_infos[i2] = CollisionInfo(fixes_hitboxes[i1], t)
    for i1 in range(len(movable_hitboxes) - 1):
        for i2 in range(i1 + 1, len(movable_hitboxes)):
            relative_speed = Vec(0, movable_hitboxes[i1].speed.y - movable_hitboxes[i2].speed.y)
            (d1, d2), t = resolve_collision(movable_hitboxes[i1], movable_hitboxes[i2], relative_speed)
            if movable_rewinds[i2] < d2:
                movable_rewinds[i2] = d2
                collisions_infos[i2] = CollisionInfo(movable_hitboxes[i1], t)
            if movable_rewinds[i1] < d1:
                movable_rewinds[i1] = d1
                collisions_infos[i1] = CollisionInfo(movable_hitboxes[i2], t)
    for i in range(len(movable_hitboxes)):
        hitbox = movable_hitboxes[i]
        d = movable_rewinds[i]
        hitbox.move(Vec(0, -hitbox.speed.y * d), with_collision_control=False)
        hitbox.add_collision_info(collisions_infos[i])
        hitbox.speed = Vec(0, 0)
