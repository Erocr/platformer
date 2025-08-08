class Drawer:
    """
    This class has all the drawing functions.

    It uses the visitor pattern, Drawer is a Visitor.
    Each draw_... function draw one type of element.
    """
    def __init__(self, view):
        self.view = view

    def draw_convex_polygon(self, convexPolygon):
        self.view.draw_polygon(convexPolygon.points)
