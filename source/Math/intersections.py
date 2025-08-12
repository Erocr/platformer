"""
Implements the intersections formulas.
You can found them on https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
"""

from Math.Vec import *


def line_line_intersection(a1, a2, b1, b2):
    """
    Returns the intersection of two lines.
    The first line is the line passing through a1 and a2. The second one is the line passing through b1 and b2.

    If there is no intersection, it returns None
    If the two lines coincide (infinity of intersections) it returns None too
    """
    denominator = (a1.x - a2.x) * (b1.y - b2.y) - (a1.y - a2.y) * (b1.x - b2.x)
    if denominator == 0:
        return None
    else:
        x = (a1.x * a2.y - a1.y * a2.x) * (b1.x - b2.x) - (a1.x - a2.x) * (b1.x * b2.y - b1.y * b2.x)
        y = (a1.x * a2.y - a1.y * a2.x) * (b1.y - b2.y) - (a1.y - a2.y) * (b1.x * b2.y - b1.y * b2.x)
        return Vec(x, y) / denominator


def segment_segment_intersection_t_u(a1, a2, b1, b2, include_borders=True):
    """
    Returns t and u so that intersection = a1 + t * (a2 - a1) and intersection = b1 + u * (b2 - b1).
    The first segment is [a1, a2]. The second one is [b1, b2].

    If there is no intersection, it returns None
    If the two lines coincide (infinity of intersections) it returns None too
    """
    denominator = (a1.x - a2.x) * (b1.y - b2.y) - (a1.y - a2.y) * (b1.x - b2.x)
    if denominator == 0:
        return None
    t = (a1.x - b1.x) * (b1.y - b2.y) - (a1.y - b1.y) * (b1.x - b2.x)
    t /= denominator
    u = -((a1.x - a2.x) * (a1.y - b1.y) - (a1.y - a2.y) * (a1.x - b1.x))
    u /= denominator
    if (0 < t < 1 and 0 < u < 1) or (include_borders and 0 <= t <= 1 and 0 <= u <= 1):
        return t, u
    else:
        return None


def segment_segment_intersection(a1, a2, b1, b2, include_borders=True):
    """
    Returns the intersection of two segments.
    The first segment is [a1, a2]. The second one is [b1, b2].

    If there is no intersection, it returns None
    If the two lines coincide (infinity of intersections) it returns None too
    """
    z = segment_segment_intersection_t_u(a1, a2, b1, b2, include_borders)
    if z is not None:
        return a1 + z[0] * (a2 - a1)
    else:
        return None


def segment_line_intersection_t(a1, a2, b1, b2, include_borders=True):
    """
    Returns t so that intersection = a1 + t * (a2 - a1).
    The segment is [a1, a2]. The line pass through b1 and b2.

    If there is no intersection, it returns None
    If the two lines coincide (infinity of intersections) it returns None too
    """
    denominator = (a1.x - a2.x) * (b1.y - b2.y) - (a1.y - a2.y) * (b1.x - b2.x)
    if denominator == 0:
        return None
    t = (a1.x - b1.x) * (b1.y - b2.y) - (a1.y - b1.y) * (b1.x - b2.x)
    t /= denominator
    if 0 < t < 1 or (include_borders and 0 <= t <= 1):
        return t
    else:
        return None


def segment_line_intersection(a1, a2, b1, b2, include_borders=True):
    """
    Returns the intersection of one segment and one line.
    The segment is [a1, a2]. The line pass through b1 and b2.

    If there is no intersection, it returns None
    If the two lines coincide (infinity of intersections) it returns None too
    """
    t = segment_line_intersection_t(a1, a2, b1, b2, include_borders)
    if t is not None:
        return a1 + t * (a2 - a1)
