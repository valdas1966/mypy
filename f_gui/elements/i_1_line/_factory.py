from f_gui.elements.i_1_line.main import Line
from f_gui.style.stroke import Stroke, DashPattern
from f_ds.geometry.point import Point


class Factory:
    """
    ========================================================================
     Factory for Line objects.
    ========================================================================
    """

    @staticmethod
    def diagonal() -> Line:
        """
        ========================================================================
         Generate a solid diagonal Line from top-left to bottom-right.
        ========================================================================
        """
        return Line(p1=Point(x=0, y=0), p2=Point(x=100, y=100))

    @staticmethod
    def arrow() -> Line:
        """
        ========================================================================
         Generate a centered horizontal arrow pointing right.
        ========================================================================
        """
        return Line(p1=Point(x=10, y=50),
                    p2=Point(x=90, y=50),
                    arrow=True)

    @staticmethod
    def dashed() -> Line:
        """
        ========================================================================
         Generate a dashed diagonal Line.
        ========================================================================
        """
        return Line(p1=Point(x=0, y=0),
                    p2=Point(x=100, y=100),
                    stroke=Stroke(pattern=DashPattern.DASHED))
